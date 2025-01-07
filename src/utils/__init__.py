## Modify 'src/utils' as per your project
## credits: aadarshlalchandani/aasetpy

import os
import time
import typing as t
from functools import wraps
from typing import List, Optional, Union

import psutil
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()

SPLIT_DELIMITER = ","


class EnvironmentVariables:
    def __getattr__(self, env_var_name):
        return getattr(settings, env_var_name.lower(), None)


env = EnvironmentVariables()
