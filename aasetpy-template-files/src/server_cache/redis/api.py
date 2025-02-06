## Modify 'src/rest_api' as per your project
## credits: aadarshlalchandani/aasetpy

from src.limits.rate_limits import (
    add_rate_limits,
    limiter,  ## Add `request: Request = None` argument to the endpoint where you want apply rate limiting using this limiter
    rate_limit_string,
)
from src.rest_api import (
    API_TITLE,
    Depends,
    FastAPI,
    HTTPException,
    Request,
    SampleResult,
    SampleUser,
    api_tags_metadata,
    sample_users_db,
)
from src.rest_api.api_security import (
    BasicAuthentication,
    BearerAuthentication,
    add_cors,
    generate_bcrypt_hash,
    verify_bcrypt_hash,
)
from src.server_cache.redis.cached_response import cache_response
from src.utils.annotations import time_spent

app = FastAPI(title=API_TITLE, openapi_tags=api_tags_metadata)
app = add_cors(app=app)
app = add_rate_limits(app=app)

jwt = BearerAuthentication()
basic_auth = BasicAuthentication()


@time_spent
@app.get("/", tags=["root"])
@limiter.limit(rate_limit_string)
def read_root(request: Request = None):
    return API_TITLE


@app.get("/basic_auth", tags=["basic auth"])
@cache_response(expire=5)
def protected_route(username: str = Depends(basic_auth.authenticate)):
    response = {
        "message": f"Hello, {username}! This is a protected route.",
        "verified": True,
        "username": username,
    }
    return response


@app.post("/sign_up", tags=["signup to get JWT"])
def sign_up(user: SampleUser, no_expire: bool = False):
    if user.username not in sample_users_db:
        sample_users_db[user.username] = generate_bcrypt_hash(user.password)

    if user.username in sample_users_db and verify_bcrypt_hash(
        password=user.password, hashed_password=sample_users_db[user.username]
    ):
        access_token = jwt.create_access_token(
            data=user.model_dump(),
            no_expire=no_expire,
        )
        return {"access_token": access_token, "token_type": "bearer"}

    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/bearer_auth", tags=["bearer auth"])
@cache_response(expire=10)
@limiter.limit(rate_limit_string)
async def bearer_auth(
    user: SampleUser = Depends(jwt.verify_token),
    request: Request = None,
):
    return SampleResult(result=[user])
