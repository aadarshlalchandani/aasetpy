from src.utils import resource_usage
from dotenv import load_dotenv

import os

load_dotenv(override=True)

AUTH_TOKEN = os.getenv("AUTH_TOKEN")

@resource_usage
def main(n: int = 5):
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    elif n == 0 or n == 1:
        return 1
    else:
        return n * main(n - 1)


if __name__ == "__main__":
    result = main()
    print(f"RESULT: {result}")
