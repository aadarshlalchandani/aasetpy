## Modify 'src/utils' as per your project
## credits: aadarshlalchandani/aasetpy

import asyncio
import inspect
import json
import os
import re
import threading
import time
import traceback
import warnings
from datetime import date, timedelta
from datetime import datetime as dtime
from functools import lru_cache, wraps
from time import perf_counter
from typing import Any, Dict, List, Optional, Tuple, Union

import psutil
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

ENCODE_ALGO = "utf8"
SPLIT_DELIMITER = "^"


def current_time():
    return dtime.now().strftime("%Y-%m-%d %H:%M:%S")


def text_splitter(text: str, split_delimiter: str = SPLIT_DELIMITER):
    return text.split(split_delimiter)


def get_batches(list_of_elements: list, batch_size: int = 150):
    batches = []
    for idx in range(0, len(list_of_elements), batch_size):
        batch = list_of_elements[idx : idx + batch_size]
        batches.append(batch)

    return batches


def preprocess_data(data: Union[List, Dict, Any]) -> Union[List, Dict, Any]:
    if isinstance(data, dict):
        return {k: preprocess_data(v) for k, v in data.items() if v}
    elif isinstance(data, list):
        return [preprocess_data(ele) for ele in data if ele]
    else:
        return data if data else None


def print_centered(statement: str, border_char: str = "-", border_char_count: int = 50):
    print(statement.center(border_char_count, border_char))


def log_error(*args: str, mininmum_length: int = 15, maximum_length: int = 170):
    """Log Errors

    Args:
        mininmum_length (int, optional): Minimum Border Length. Defaults to 15.
        maximum_length (int, optional): Maximum Border Length. Defaults to 170.
    """
    max_length = max(
        min(max([len(str(stmt)) for stmt in args]), maximum_length), mininmum_length
    )
    print_centered(" ERROR ", border_char="✖", border_char_count=max_length)
    for stmt in args:
        print(stmt)
    print_centered(" ERROR ", border_char="✖", border_char_count=max_length)
    return
