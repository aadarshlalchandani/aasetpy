## Modify 'main.py' as per your project
## credits: aadarshlalchandani/aasetpy

from src.utils import lru_cache
from src.utils.annotations import monitor_usage
from src.utils.environment_variables import env


@monitor_usage
def main():
    return get_factorial(n=5, auth_token=env("AUTH_TOKEN", "token"))


@lru_cache
def get_factorial(n: int, auth_token: str):

    if n < 0:
        raise ValueError("n must be a non-negative integer")

    elif n == 0 or n == 1:
        if auth_token == env.AUTH_TOKEN:
            print("AUTH_TOKEN Verified!")

        else:
            print("Wrong AUTH_TOKEN Entered..")

        return 1

    else:
        return n * get_factorial(n - 1, auth_token=auth_token)


if __name__ == "__main__":
    result = main()
    print(f"RESULT: {result}")
