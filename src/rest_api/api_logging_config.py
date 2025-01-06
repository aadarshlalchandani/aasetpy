## Modify 'src/rest_api' as per your project
## credits: aadarshlalchandani/aasetpy

from uvicorn.config import LOGGING_CONFIG


def get_logging_config():
    default_datetime_format = "%Y-%m-%d %H:%M:%S"
    LOGGING_CONFIG["formatters"]["default"]["datefmt"] = default_datetime_format
    LOGGING_CONFIG["formatters"]["access"]["datefmt"] = default_datetime_format
    LOGGING_CONFIG["formatters"]["default"][
        "fmt"
    ] = "%(asctime)s %(levelprefix)s %(message)s"
    LOGGING_CONFIG["formatters"]["access"]["fmt"] = (
        '%(asctime)s %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'
        + f"\n{'-'*50}\n"
    )
    return LOGGING_CONFIG
