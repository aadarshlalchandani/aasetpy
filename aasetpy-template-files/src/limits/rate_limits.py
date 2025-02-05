from src.limits import (
    FastAPI,
    Limiter,
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
    env,
    get_remote_address,
)

n_requests = env.LIMIT_N_REQUESTS
limit_time_unit = env.LIMIT_TIME_UNIT

"""
# Rate Limit String Notation: [count] [per|/] [n (optional)] [second|minute|hour|day|month|year]

10 per hour
10/hour
10/hour;100/day;2000 per year
100/day, 500/7days
"""
rate_limit_string = f"{n_requests}/{limit_time_unit}"
default_rate_limit = "10/minute"

## Add `request: Request = None` argument to the endpoint where you want apply rate limiting using this limiter
limiter = Limiter(key_func=get_remote_address, default_limits=[default_rate_limit])


def add_rate_limits(app: FastAPI):
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    return app
