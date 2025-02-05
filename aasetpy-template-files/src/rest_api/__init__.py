## Modify 'src/rest_api' as per your project
## credits: aadarshlalchandani/aasetpy

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status, Request

from src.utils import (
    SPLIT_DELIMITER,
    BaseModel,
    List,
)
from src.utils.environment_variables import env

template_credits = "aadarshlalchandani/aasetpy"

API_HOST = env.API_HOST
API_PORT = int(env.API_PORT)
API_TITLE = f"REST API Template by '{template_credits}'"

api_tags_metadata = [
    {
        "name": "root",
        "description": f"Home Page of the Sample REST API by '{template_credits}'",
    },
    {
        "name": "basic auth",
        "description": "Basic Authentication for REST API",
    },
    {
        "name": "signup to get JWT",
        "description": "SignUp Endpoint to generate JWT for given User",
    },
    {
        "name": "bearer auth",
        "description": "Sample Response for the User inside JWT",
    },
]


sample_users_db = {}


class SampleUser(BaseModel):
    username: str = "testuser"
    password: str = "testpassword"


class SampleResult(BaseModel):
    result: list
