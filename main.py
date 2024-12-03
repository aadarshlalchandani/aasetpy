from src.utils import resource_usage


@resource_usage
def test_factorial(n):
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    elif n == 0 or n == 1:
        return 1
    else:
        return n * test_factorial(n - 1)


if __name__ == "__main__":
    result = test_factorial(5)
    print(f"RESULT: {result}")
