## Modify 'src/utils' as per your project
## credits: aadarshlalchandani/aasetpy

import os
import time
from functools import wraps

import psutil
from dotenv import load_dotenv

load_dotenv(override=True)

AUTH_TOKEN = os.getenv("AUTH_TOKEN")
