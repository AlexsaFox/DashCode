from aioredis import Redis
from fastapi import Request

from src.types import AppState


async def get_cache(request: Request) -> Redis:
    app_state: AppState = request.app.app_state

    return app_state.cache
