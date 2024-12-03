from src.utils import resource_usage


@resource_usage
def main(n: int = 5):
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    elif n == 0 or n == 1:
        return 1
    else:
        return n * test_factorial(n - 1)


if __name__ == "__main__":
    result = main()
    print(f"RESULT: {result}")
