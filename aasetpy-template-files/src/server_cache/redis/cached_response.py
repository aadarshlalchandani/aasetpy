## Modify 'src/server_cache' as per your project
## credits: aadarshlalchandani/aasetpy

from src.server_cache import (
    DEFAULT_CACHE_EXPIRE_SECONDS,
    BaseModel,
    Request,
    iscoroutinefunction,
    json,
    signature,
    wraps,
)
from src.server_cache.redis import get_redis_client


def cache_response(
    expire: int = DEFAULT_CACHE_EXPIRE_SECONDS,
    drop_keys: list = ["token", "request"],
):
    """### Usage:

    ```
    @cache_response()  
    def func():  
        return None
    ```
    #### ~ OR ~
    ```
    @cache_response(expire=600)  
    def func():  
        return None
    ```
    """
    redis_client = get_redis_client()

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            params = signature(func).parameters

            param_dict = {}
            request = None
            for i, (name, param) in enumerate(params.items()):
                if i < len(args):
                    if isinstance(args[i], Request):
                        request = args[i]
                    elif isinstance(args[i], BaseModel):
                        param_dict[name] = args[i].dict()
                    else:
                        param_dict[name] = args[i]
                elif name in kwargs:
                    if isinstance(kwargs[name], BaseModel):
                        param_dict[name] = kwargs[name].dict()
                    else:
                        param_dict[name] = kwargs[name]
                elif param.default is not param.empty:
                    param_dict[name] = param.default

            [param_dict.pop(key) for key in drop_keys if key in param_dict]

            if request and request.method == "POST":
                body = request.json()
                param_dict.update(body)

            cache_key = (
                f"{func.__name__}:{json.dumps(param_dict, sort_keys=True, default=str)}"
            )

            cached_response = redis_client.get(cache_key)
            if cached_response:
                print("CACHE HIT!")
                return json.loads(cached_response)

            if iscoroutinefunction(func):
                response = await func(*args, **kwargs)
            else:
                response = func(*args, **kwargs)

            redis_client.setex(cache_key, expire, json.dumps(response, default=str))

            return response

        return wrapper

    return decorator
