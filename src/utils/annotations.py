## Modify 'src/utils' as per your project
## credits: aadarshlalchandani/aasetpy

from . import psutil, time, wraps


def time_spent(func):
    """
    A decorator function to calculate the total time spent by any function to execute.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The decorated function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        total_time = end_time - start_time

        print(f"Time Taken by '{func.__name__}': {total_time:.2f} seconds.")
        print()

        return result

    return wrapper


def resource_usage(func):
    """Get stats for resources used by a function

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The decorated function.
    """

    @time_spent
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get system information
        logical_cpu_count = psutil.cpu_count(logical=True)
        memory_info = psutil.virtual_memory()

        total_ram = round(memory_info.total / (1024**3), 2)

        # Start measuring CPU and RAM usage
        start_cpu_percent = psutil.cpu_percent(interval=1)
        start_memory_usage = memory_info.used

        # Call the function
        result = func(*args, **kwargs)

        # End measuring CPU and RAM usage
        end_cpu_percent = psutil.cpu_percent(interval=1)
        end_memory_usage = psutil.virtual_memory().used

        # Calculate average CPU and RAM usage
        avg_cpu_usage = round((start_cpu_percent + end_cpu_percent) / 2, 2)
        avg_memory_usage = round(
            ((start_memory_usage + end_memory_usage) / 2) / (1024**3), 2
        )
        pct_memory_used = round((avg_memory_usage / total_ram) * 100, 2)

        usage_statement = f"Average CPU Usage: {avg_cpu_usage}% of {logical_cpu_count} Cores\nAverage Memory Usage: {avg_memory_usage} GB ({pct_memory_used}%) of {total_ram} GB.\n"

        print(usage_statement)

        return result

    return wrapper
