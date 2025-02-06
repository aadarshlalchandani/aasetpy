## Modify 'src/server_cache' as per your project
## credits: aadarshlalchandani/aasetpy

import asyncio
import json
import time
from functools import wraps
from inspect import iscoroutinefunction, signature

from src.utils.environment_variables import env

DEFAULT_CACHE_EXPIRE_SECONDS = env.DEFAULT_CACHE_EXPIRE_SECONDS
