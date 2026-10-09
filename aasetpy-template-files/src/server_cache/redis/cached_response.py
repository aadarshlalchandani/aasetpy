## Modify 'src/server_cache' as per your project
## credits: aadarshlalchandani/aasetpy

from src.server_cache import (
    DEFAULT_CACHE_EXPIRE_SECONDS,
    BaseModel,
    JSONResponse,
    Request,
    b64_encode,
    iscoroutinefunction,
    json,
    signature,
    wraps,
)
from src.server_cache.redis import get_redis_client

redis_client = get_redis_client()


def cache_response(
    expire: int = DEFAULT_CACHE_EXPIRE_SECONDS,
    drop_keys: list = ["token", "request", "credentials", "creds"],
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

    def decorator(func):
        is_async = iscoroutinefunction(func)

        def get_param_dict(*args, **kwargs):
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

            for key in drop_keys:
                param_dict.pop(key, None)

            return param_dict, request

        def get_cache_key(param_dict):
            return f"{func.__name__}:{b64_encode(json.dumps(param_dict, sort_keys=True, default=str))}"

        def set_cache(cache_key, response):
            if isinstance(response, JSONResponse):
                redis_client.setex(cache_key, expire, response.body.decode("utf-8"))
            else:
                redis_client.setex(cache_key, expire, json.dumps(response, default=str))

        if is_async:

            @wraps(func)
            async def wrapper(*args, **kwargs):
                request: Request
                param_dict, request = get_param_dict(*args, **kwargs)

                if request and request.method == "POST":
                    try:
                        body = await request.json()
                        param_dict.update(body)
                    except Exception:
                        pass

                cache_key = get_cache_key(param_dict)
                cached_response = redis_client.get(cache_key)
                if cached_response:
                    cresponse = json.loads(cached_response)
                    print(f"CACHE HIT '{func.__name__}'!\n")
                    return cresponse

                response = await func(*args, **kwargs)
                set_cache(cache_key, response)
                return response

        else:

            @wraps(func)
            def wrapper(*args, **kwargs):
                request: Request
                param_dict, request = get_param_dict(*args, **kwargs)

                if request and request.method == "POST":
                    try:
                        body = request.json()
                        param_dict.update(body)
                    except Exception:
                        pass

                # Note: Sync wrapper cannot await request.json()
                cache_key = get_cache_key(param_dict)
                cached_response = redis_client.get(cache_key)
                if cached_response:
                    cresponse = json.loads(cached_response)
                    print(f"CACHE HIT '{func.__name__}'!\n")
                    return cresponse

                response = func(*args, **kwargs)
                set_cache(cache_key, response)
                return response

        return wrapper

    return decorator
