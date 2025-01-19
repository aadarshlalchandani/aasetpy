## Modify 'api.py' as per your project
## credits: aadarshlalchandani/aasetpy

if __name__ == "__main__":
    from src.rest_api import API_HOST, API_PORT, uvicorn
    from src.rest_api.api import app
    from src.rest_api.api_logging_config import get_logging_config

    uvicorn.run(
        app=app,
        port=API_PORT,
        host=API_HOST,
        log_config=get_logging_config(),
    )
