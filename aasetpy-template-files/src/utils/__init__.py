## Modify 'src/utils' as per your project
## credits: aadarshlalchandani/aasetpy

import datetime
import inspect
import json
import os
import re
import threading
import time
import typing as t
from datetime import datetime as dtime
from datetime import timedelta
from functools import lru_cache, wraps
from typing import Any, Dict, List, Optional, Union

import psutil
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

ENCODE_ALGO = "utf8"
SPLIT_DELIMITER = ","


def text_splitter(text: str, split_delimiter: str = SPLIT_DELIMITER):
    return text.split(split_delimiter)
