from src.utils import AUTH_TOKEN
from src.utils.annotations import resource_usage


@resource_usage
def main():
    return None


@resource_usage
def get_factorial(n: int, auth_token: str):
    if auth_token == AUTH_TOKEN:
        print("AUTH_TOKEN Verified!")
    else:
        print("Wrong AUTH_TOKEN Entered..")

    if n < 0:
        raise ValueError("n must be a non-negative integer")
    elif n == 0 or n == 1:
        return 1
    else:
        return n * get_factorial(n - 1, auth_token=auth_token)


if __name__ == "__main__":
    result = get_factorial(n=5, auth_token="token")
    print(f"RESULT: {result}")
