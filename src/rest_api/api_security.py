## Modify 'src/rest_api' as per your project
## credits: aadarshlalchandani/aasetpy

import secrets

import jwt
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
)

from src.rest_api import Depends, FastAPI, HTTPException, status
from src.utils import datetime, dtime, text_splitter, timedelta
from src.utils.environment_variables import env

basic_auth = HTTPBasic()
bearer_auth = HTTPBearer()


def add_cors(app: FastAPI):
    from fastapi.middleware.cors import CORSMiddleware

    allowed_origins = text_splitter(env.API_ALLOWED_ORIGINS)
    allowed_methods = text_splitter(env.API_ALLOWED_METHODS)
    allowed_headers = text_splitter(env.API_ALLOWED_HEADERS)
    allow_credentials = True

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=allow_credentials,
        allow_methods=allowed_methods,
        allow_headers=allowed_headers,
    )
    return app


class BasicAuthentication:
    def __init__(self):
        self.correct_username = env.API_BASIC_AUTH_USERNAME
        self.correct_password = env.API_BASIC_AUTH_PASSWORD
        self.encode_algo = "utf8"

    def authenticate(self, credentials: HTTPBasicCredentials = Depends(basic_auth)):
        is_correct_username = secrets.compare_digest(
            credentials.username.encode(self.encode_algo),
            self.correct_username.encode(self.encode_algo),
        )
        is_correct_password = secrets.compare_digest(
            credentials.password.encode(self.encode_algo),
            self.correct_password.encode(self.encode_algo),
        )

        if not (is_correct_username and is_correct_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Basic"},
            )
        return credentials.username


class BearerAuthentication:
    def __init__(self):
        self.secret_key = env.API_JWT_SECRET_KEY
        self.algorithm = env.API_JWT_ENCRYPTION_ALGORITHM
        self.jwt_expire_seconds = float(env.API_JWT_EXPIRE_SECONDS)

    def create_access_token(self, data: dict, no_expire: bool = False):
        to_encode = data.copy()
        if not no_expire:
            exp = dtime.now(datetime.timezone.utc) + timedelta(
                seconds=self.jwt_expire_seconds
            )
            to_encode.update({"exp": exp})

        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(
        self, credentials: HTTPAuthorizationCredentials = Depends(bearer_auth)
    ):
        try:
            payload = jwt.decode(
                jwt=credentials.credentials,
                key=self.secret_key,
                algorithms=[self.algorithm],
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
