from aioredis import Redis
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from .config import Configuration


class AppState:
    cache: Redis
    config: Configuration
    engine: AsyncEngine


class ExpectedError(ValueError):
    pass
