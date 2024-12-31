## Modify 'src/utils' as per your project
## credits: aadarshlalchandani/aasetpy

import os
import time
import psutil

from functools import wraps
from dotenv import load_dotenv

load_dotenv(override=True)

AUTH_TOKEN = os.getenv("AUTH_TOKEN")
