## Modify 'src/server_cache' as per your project
## credits: aadarshlalchandani/aasetpy

from src.server_cache import (
    DEFAULT_CACHE_EXPIRE_SECONDS,
    asyncio,
    iscoroutinefunction,
    json,
    signature,
    wraps,
)
from src.server_cache.redis import get_redis_client


def cache_response(expire: int = DEFAULT_CACHE_EXPIRE_SECONDS):
    redis_client = get_redis_client()

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            params = signature(func).parameters

            param_dict = {}
            for i, (name, param) in enumerate(params.items()):
                if i < len(args):
                    param_dict[name] = args[i]
                elif name in kwargs:
                    param_dict[name] = kwargs[name]
                elif param.default is not param.empty:
                    param_dict[name] = param.default
            param_dict.pop("request", None)

            cache_key = f"{func.__name__}:{json.dumps(param_dict, sort_keys=True)}"

            cached_response = redis_client.get(cache_key)
            if cached_response:
                return json.loads(cached_response)

            response = func(*args, **kwargs)

            if asyncio.iscoroutine(response):
                response = asyncio.get_event_loop().run_until_complete(response)

            redis_client.setex(cache_key, expire, json.dumps(response))

            return response

        if iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                return await asyncio.to_thread(wrapper, *args, **kwargs)

            return async_wrapper

        return wrapper

    return decorator
