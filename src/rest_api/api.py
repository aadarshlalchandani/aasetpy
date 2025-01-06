## Modify 'src/rest_api' as per your project
## credits: aadarshlalchandani/aasetpy

from src.rest_api import (
    API_TITLE,
    Depends,
    FastAPI,
    SampleRequest,
    SampleResult,
    api_tags_metadata,
)
from src.rest_api.api_authentication import add_cors, get_token
from src.utils.annotations import time_spent

app = FastAPI(title=API_TITLE, openapi_tags=api_tags_metadata)
app = add_cors(app=app)


@time_spent
@app.get("/", tags=["root"])
def read_root():
    return API_TITLE


@app.post("/sampleresult", tags=["sample result"])
async def sample_result(param: SampleRequest, token: str = Depends(get_token)):
    response = param.param
    return SampleResult(result=[response])
