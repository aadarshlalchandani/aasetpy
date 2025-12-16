## Modify 'src/server_cache' as per your project
## credits: aadarshlalchandani/aasetpy

from redis import ConnectionPool, Redis

from src.server_cache import env

pool = ConnectionPool(
    host=env("CACHE_HOST", "localhost"),
    port=int(env("CACHE_PORT", 6379)),
    db=int(env("CACHE_DB", 0)),
    max_connections=int(env("CACHE_MAX_CONNECTIONS", 3)),
)


def get_redis_client():
    redis_client = Redis(connection_pool=pool)
    return redis_client


def flush_redis_db():
    get_redis_client().flushdb()
