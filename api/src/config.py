import os
from typing import Any, Literal, cast
from dynaconf import Dynaconf

from pydantic import BaseModel, PositiveInt, RedisDsn, StrictBool, StrictStr


ENVIRONMENT = Literal['development', 'testing', 'production']
BASE_DIR = os.getcwd()


class AppConfiguration(BaseModel):
    title: StrictStr
    description: StrictStr


class CacheConfiguration(BaseModel):
    dsn: RedisDsn
    expire_minutes: PositiveInt


class DatabaseConfiguration(BaseModel):
    dsn: StrictStr


class ServerConfiguration(BaseModel):
    host: StrictStr
    port: PositiveInt


class JWTConfiguration(BaseModel):
    algorithm: StrictStr
    expire_hours: PositiveInt


class BaseSuperuser(BaseModel):
    username: StrictStr
    password: StrictStr
    email: StrictStr


class Configuration(BaseModel):
    app: AppConfiguration
    base_superuser: BaseSuperuser
    cache: CacheConfiguration
    database: DatabaseConfiguration
    debug: StrictBool
    environment: StrictStr
    jwt: JWTConfiguration
    secret_key: StrictStr
    server: ServerConfiguration


def load_configuration(env: ENVIRONMENT | None = None) -> Configuration:
    if env is None:
        env = cast(ENVIRONMENT, os.getenv('DYNACONF_ENV', 'development'))

    settings = Dynaconf(
        settings_files=['default.yaml', f'{env}.yaml', '.secrets.yaml'],
        load_dotenv=True,
        merge_enabled=True,
        root_path=os.path.join(BASE_DIR, 'config'),
    )

    config: dict[str, Any] = {'environment': env}
    for key in Configuration.__fields__.keys():
        if settings.get(key) is not None:
            config[key] = settings[key]

    return Configuration(**config)
