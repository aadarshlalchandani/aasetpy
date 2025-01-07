## Modify 'src/rest_api' as per your project
## credits: aadarshlalchandani/aasetpy

import uvicorn
from fastapi import Depends, FastAPI, HTTPException

from src.utils import (
    SPLIT_DELIMITER,
    BaseModel,
    List,
    env,
)

template_credits = "aadarshlalchandani/aasetpy"

API_HOST = env.API_HOST
API_PORT = int(env.API_PORT)
API_TITLE = f"REST API Template by {template_credits}"

api_tags_metadata = [
    {
        "name": "root",
        "description": f"Home Page of the Sample REST API by '{template_credits}'",
    },
    {
        "name": "sample result",
        "description": "Sample Response with Bearer Token Authentication",
    },
]


class SampleRequest(BaseModel):
    param: str = template_credits


class SampleResult(BaseModel):
    result: list
