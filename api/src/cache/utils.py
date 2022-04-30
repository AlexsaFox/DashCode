from aioredis import Redis, from_url

from src.config import CacheConfiguration


def get_cache_backend(config: CacheConfiguration) -> Redis:
    connection: Redis = from_url(config.dsn, encoding='utf-8', decode_responses=False)
    return connection
