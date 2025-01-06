## Modify 'src/utils' as per your project
## credits: aadarshlalchandani/aasetpy

import os
import time
import typing as t
from functools import wraps
from typing import List, Optional, Union

import psutil
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv(override=True)

SPLIT_DELIMITER = ","


def get_credentials(key: str):
    return os.environ.get(key)
