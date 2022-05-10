from tempfile import mkdtemp
from typing import AsyncGenerator

import pytest
from _pytest.config import Config
from aioredis import Redis
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from pydantic import RedisDsn
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

from src.auth.utils import create_user, generate_jwt
from src.cache.utils import get_cache_backend
from src.config import Configuration, load_configuration
from src.create_app import App, create_app
from src.db.models import Base, User
from src.db.utils import get_engine
from tests.utils import GraphQLClient


database_container = pytest.StashKey[PostgresContainer]()
cache_container = pytest.StashKey[RedisContainer]()


def pytest_configure(config: Config) -> None:
    config.stash[database_container] = PostgresContainer(
        image='postgres',
        user='user',
        password='password',
        dbname='backend',
    )
    config.stash[database_container].start()

    config.stash[cache_container] = RedisContainer(image='redis')
    config.stash[cache_container].start()


def pytest_unconfigure(config: Config) -> None:
    config.stash[database_container].stop()
    config.stash[cache_container].stop()


@pytest.fixture
def test_config(pytestconfig: Config) -> Configuration:
    config = load_configuration('testing')
    config.file_upload.upload_path = mkdtemp()
    config.database.dsn = (
        pytestconfig.stash[database_container]
        .get_connection_url()
        .replace('psycopg2', 'asyncpg')
    )
    redis_port = pytestconfig.stash[cache_container].get_exposed_port(
        pytestconfig.stash[cache_container].port_to_expose
    )
    config.cache.dsn = RedisDsn(f'redis://localhost:{redis_port}', scheme='redis')
    return config


@pytest.fixture
async def database_engine(test_config: Configuration) -> AsyncEngine:
    engine = get_engine(test_config.database)
    return engine


@pytest.fixture
async def cache(test_config: Configuration) -> Redis:
    return get_cache_backend(test_config.cache)


@pytest.fixture
async def app(
    test_config: Configuration, database_engine: AsyncEngine
) -> AsyncGenerator[App, None]:
    async with database_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    app = create_app(test_config)
    async with LifespanManager(app):
        yield app

    async with database_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def database_session(app: App) -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(app.app_state.engine) as session:
        yield session


@pytest.fixture
async def client(app: App) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://localhost') as async_client:
        yield async_client


@pytest.fixture
async def user(database_session: AsyncSession) -> User:
    username = 'user'
    email = 'user@mail.com'
    password = 'password'
    user = await database_session.run_sync(create_user, username, email, password)
    return user


@pytest.fixture
def graphql_client(client: AsyncClient) -> GraphQLClient:
    return GraphQLClient(client)


@pytest.fixture
def token_user(test_config: Configuration, user: User) -> tuple[str, User]:
    return generate_jwt(test_config, user), user
