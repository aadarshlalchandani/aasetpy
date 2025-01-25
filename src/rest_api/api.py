## Modify 'src/rest_api' as per your project
## credits: aadarshlalchandani/aasetpy


from src.rest_api import (
    API_TITLE,
    Depends,
    FastAPI,
    HTTPException,
    SampleResult,
    SampleUser,
    api_tags_metadata,
    sample_users_db,
)
from src.rest_api.api_security import (
    BasicAuthentication,
    BearerAuthentication,
    add_cors,
)
from src.utils.annotations import time_spent

app = FastAPI(title=API_TITLE, openapi_tags=api_tags_metadata)
app = add_cors(app=app)

jwt = BearerAuthentication()
basic_auth = BasicAuthentication()


@time_spent
@app.get("/", tags=["root"])
def read_root():
    return API_TITLE


@app.get("/basic_auth", tags=["basic auth"])
def protected_route(username: str = Depends(basic_auth.authenticate)):
    response = {
        "message": f"Hello, {username}! This is a protected route.",
        "verified": True,
        "username": username,
    }
    return response


@app.post("/sign_up", tags=["signup to get JWT"])
def sign_up(user: SampleUser, no_expire: bool = False):
    if (
        user.username in sample_users_db
        and sample_users_db[user.username] == user.password
    ):
        access_token = jwt.create_access_token(
            data=user.model_dump(),
            no_expire=no_expire,
        )
        return {"access_token": access_token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/bearer_auth", tags=["bearer auth"])
async def bearer_auth(user: SampleUser = Depends(jwt.verify_token)):
    return SampleResult(result=[user])
