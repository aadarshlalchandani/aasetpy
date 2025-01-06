## Modify 'src/rest_api' as per your project
## credits: aadarshlalchandani/aasetpy

from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from src.rest_api import (
    SPLIT_DELIMITER,
    BaseModel,
    Depends,
    FastAPI,
    HTTPException,
    get_credentials,
)
from src.utils import t

API_AUTH_TOKENS = get_credentials("API_AUTH_TOKEN").split(SPLIT_DELIMITER)
known_tokens = set(API_AUTH_TOKENS)
get_bearer_token = HTTPBearer(auto_error=False)


class UnauthorizedMessage(BaseModel):
    detail: str = "Bearer token missing or unknown"


def get_token(
    auth: t.Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),
) -> str:
    if auth is None or (token := auth.credentials) not in known_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=UnauthorizedMessage().detail,
        )
    return token


def add_cors(app: FastAPI):
    allowed_origins = get_credentials("API_ALLOWED_ORIGINS").split(SPLIT_DELIMITER)
    allowed_methods = get_credentials("API_ALLOWED_METHODS").split(SPLIT_DELIMITER)
    allowed_headers = get_credentials("API_ALLOWED_HEADERS").split(SPLIT_DELIMITER)
    allow_credentials = True

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=allow_credentials,
        allow_methods=allowed_methods,
        allow_headers=allowed_headers,
    )
    return app
