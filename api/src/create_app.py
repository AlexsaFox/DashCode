from typing import Callable, Coroutine, cast
from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.auth.utils import create_user
from src.config import Configuration
from src.cache.utils import get_cache_backend
from src.db.utils import get_engine
from src.db.models import User
from src.graphql.schema import graphql_app
from src.routes import router
from src.types import AppState


class App(FastAPI):
    app_state: AppState


def create_startup_hook(app: App) -> Callable[[], Coroutine[None, None, None]]:
    async def startup_hook() -> None:
        app.app_state.cache = get_cache_backend(app.app_state.config.cache)

        app.app_state.engine = get_engine(app.app_state.config.database)
        async with AsyncSession(app.app_state.engine) as session:
            base_superuser = app.app_state.config.base_superuser
            query = await session.execute(
                select(User).filter_by(username=base_superuser.username)
            )
            user: User | None = query.first()
            if user is None:
                await session.run_sync(
                    create_user,
                    base_superuser.username,
                    base_superuser.email,
                    base_superuser.password,
                    True,
                )

    return startup_hook


def create_shutdown_hook(app: App) -> Callable[[], Coroutine[None, None, None]]:
    async def shutdown_hook() -> None:
        if app.app_state.cache is not None:
            await app.app_state.cache.close()
            await app.app_state.cache.connection_pool.disconnect()
        if app.app_state.engine is not None:
            await app.app_state.engine.dispose()

    return shutdown_hook


def create_app(config: Configuration) -> App:
    app: App = cast(
        App,
        FastAPI(
            title=config.app.title,
            description=config.app.description,
            debug=config.debug,
        ),
    )
    app.app_state = AppState()
    app.app_state.config = config

    app.include_router(router)
    app.include_router(graphql_app, prefix='/graphql')

    app.router.add_event_handler('startup', create_startup_hook(app))
    app.router.add_event_handler('shutdown', create_shutdown_hook(app))

    return app
