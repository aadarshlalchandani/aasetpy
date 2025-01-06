## Modify 'src/utils' as per your project
## credits: aadarshlalchandani/aasetpy

import os
import time
from functools import wraps

import psutil
from dotenv import load_dotenv

load_dotenv(override=True)

get_credentials = lambda key: os.environ.get(key)

AUTH_TOKEN = get_credentials("AUTH_TOKEN")
