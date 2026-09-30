## Modify 'src/server_cache' as per your project
## credits: aadarshlalchandani/aasetpy

from inspect import iscoroutinefunction, signature

from fastapi import Request
from fastapi.responses import JSONResponse

from src.utils import Basemodel, env, json, time, wraps

DEFAULT_CACHE_EXPIRE_SECONDS: int = int(env("DEFAULT_CACHE_EXPIRE_SECONDS", "86400"))
