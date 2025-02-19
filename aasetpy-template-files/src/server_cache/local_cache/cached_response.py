from src.server_cache.local_cache import (
    DEFAULT_CACHE_EXPIRE_SECONDS,
    TTLCache,
    cached,
    env,
    hashlib,
    json,
    time,
    wraps,
)

cache_settings = TTLCache(
    maxsize=int(env("CACHE_MAXSIZE", "500")), ttl=DEFAULT_CACHE_EXPIRE_SECONDS
)


def make_hashable(*args, **kwargs):
    def serialize(obj):
        if isinstance(obj, (int, float, str, bool, type(None))):
            return obj
        elif isinstance(obj, (list, tuple)):
            return [serialize(item) for item in obj]
        elif isinstance(obj, dict):
            return {
                str(key): serialize(value)
                for key, value in obj.items()
                if key != "request"
            }
        else:
            return str(obj)

    # Remove 'request' from kwargs before serialization
    kwargs_without_request = {k: v for k, v in kwargs.items() if k != "request"}

    serialized = json.dumps(
        (serialize(args), serialize(kwargs_without_request)), sort_keys=True
    )
    return hashlib.md5(serialized.encode()).hexdigest()


def print_cache_hit(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        key = make_hashable(*args, **kwargs)
        if key in cache_settings:
            end_time = time.time()
            cache_settings[key]["response"]["total_time_taken_seconds"] = round(
                end_time - start_time, 5
            )
            return cache_settings[key]

        else:
            result = await func(*args, **kwargs)
            cache_settings[key] = result
            return result

    return wrapper


def cache_response(func):
    """### Usage

    ```
    @cache_response
    def func():  
        return None
    ```
    """
    cached_func = cached(cache_settings, key=make_hashable)(func)
    return print_cache_hit(cached_func)
