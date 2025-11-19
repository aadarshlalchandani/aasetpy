## Modify 'src/utils' as per your project
## credits: aadarshlalchandani/aasetpy

import asyncio
import datetime
import inspect
import json
import os
import re
import threading
import time
from datetime import datetime as dtime
from datetime import timedelta
from functools import lru_cache, wraps
from typing import Any, Dict, List, Optional, Union

import psutil
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

ENCODE_ALGO = "utf8"
SPLIT_DELIMITER = "^"


def text_splitter(text: str, split_delimiter: str = SPLIT_DELIMITER):
    return text.split(split_delimiter)


def get_batches(list_of_elements: list, batch_size: int = 150):
    batches = []
    for idx in range(0, len(list_of_elements), batch_size):
        batch = list_of_elements[idx : idx + batch_size]
        batches.append(batch)

    return batches


def preprocess_dict(dictionary: Dict):
    return {k: v for k, v in dictionary.items()}
