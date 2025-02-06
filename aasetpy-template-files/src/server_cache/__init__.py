## Modify 'src/server_cache' as per your project
## credits: aadarshlalchandani/aasetpy

import json
import time
from functools import wraps
from inspect import iscoroutinefunction, signature

from src.rest_api import BaseModel, Request
from src.utils.environment_variables import env

DEFAULT_CACHE_EXPIRE_SECONDS = env.DEFAULT_CACHE_EXPIRE_SECONDS
