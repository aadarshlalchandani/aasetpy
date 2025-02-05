## Modify 'src/limits' as per your project
## credits: aadarshlalchandani/aasetpy

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from src.rest_api import FastAPI
from src.utils.environment_variables import env
