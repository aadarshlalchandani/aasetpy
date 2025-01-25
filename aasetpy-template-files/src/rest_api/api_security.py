## Modify 'src/rest_api' as per your project
## credits: aadarshlalchandani/aasetpy

import secrets

import bcrypt
import jwt
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
)

from src.rest_api import Depends, FastAPI, HTTPException, status
from src.utils import ENCODE_ALGO, datetime, dtime, text_splitter, timedelta
from src.utils.environment_variables import env

basic_auth = HTTPBasic()
bearer_auth = HTTPBearer()


def generate_bcrypt_hash(password: str, rounds: int = 12) -> str:
    password_bytes = password.encode(ENCODE_ALGO)
    salt = bcrypt.gensalt(rounds=rounds)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode(ENCODE_ALGO)


def verify_bcrypt_hash(password: str, hashed_password: str) -> bool:
    password_bytes = password.encode(ENCODE_ALGO)
    hashed_bytes = hashed_password.encode(ENCODE_ALGO)
    return bcrypt.checkpw(password_bytes, hashed_bytes)


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
        self.correct_password = generate_bcrypt_hash(env.API_BASIC_AUTH_PASSWORD)

    def authenticate(self, credentials: HTTPBasicCredentials = Depends(basic_auth)):
        is_correct_username = secrets.compare_digest(
            credentials.username.encode(ENCODE_ALGO),
            self.correct_username.encode(ENCODE_ALGO),
        )
        is_correct_password = verify_bcrypt_hash(
            credentials.password,
            self.correct_password,
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
