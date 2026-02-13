## Modify 'src/utils' as per your project
## credits: aadarshlalchandani/aasetpy

from pynvml import (
    NVMLError,
    nvmlDeviceGetComputeRunningProcesses,
    nvmlDeviceGetCount,
    nvmlDeviceGetHandleByIndex,
    nvmlDeviceGetMemoryInfo,
    nvmlDeviceGetName,
    nvmlDeviceGetUtilizationRates,
    nvmlInit,
    nvmlShutdown,
)

from src.utils import (
    asyncio,
    inspect,
    json,
    os,
    perf_counter,
    psutil,
    threading,
    time,
    wraps,
)


def get_file_path(filename):
    return os.path.abspath(filename)


def get_program_pid(script_path: str, filename: str):
    process_entities = ["pid", "name", "cmdline"]
    processes = psutil.process_iter(process_entities)
    program_pid = [
        process.info["pid"]
        for process in processes
        if script_path in process.info["cmdline"] or filename in process.info["cmdline"]
    ][0]
    return program_pid


def get_program_usage(pid: int, interval: float = 1.0):
    cpu_usage = []
    ram_usage = []
    gpu_utilization = []
    gpu_memory_usage = []
    gpu_name = []

    stop_monitoring = threading.Event()

    def monitor():
        process = psutil.Process(pid)

        # Initialize NVML
        try:
            nvmlInit()
            gpu_count = nvmlDeviceGetCount()
            print(
                f"{gpu_count} NVIDIA GPU(s) found. Will monitor the usage of the first GPU.\n"
            )
            handle = nvmlDeviceGetHandleByIndex(0)
        except NVMLError as e:
            print(f"NVML Init failed: {e}")
            return

        while not stop_monitoring.is_set():
            try:
                # CPU and RAM
                cpu_usage.append(process.cpu_percent(interval=interval))
                ram_usage.append(process.memory_percent())

                # GPU Util and Memory
                try:
                    processes = nvmlDeviceGetComputeRunningProcesses(handle)
                    for p in processes:
                        if p.pid == pid:
                            mem = nvmlDeviceGetMemoryInfo(handle)
                            gpu_memory_usage.append(mem.used)
                    util = nvmlDeviceGetUtilizationRates(handle)
                    gpu_utilization.append(util.gpu)
                    gpu_name_value = nvmlDeviceGetName(handle).decode("utf-8")
                    (
                        gpu_name.append(gpu_name_value)
                        if gpu_name_value not in gpu_name
                        else None
                    )
                except NVMLError:
                    print("nvml error get compute running processes")
                    pass

            except (psutil.NoSuchProcess, KeyboardInterrupt):
                break

            time.sleep(interval)

        nvmlShutdown()

    monitor_thread = threading.Thread(target=monitor)
    monitor_thread.start()

    def stop_monitoring_func():
        stop_monitoring.set()
        monitor_thread.join()

    return (
        stop_monitoring_func,
        cpu_usage,
        ram_usage,
        gpu_utilization,
        gpu_memory_usage,
        gpu_name,
    )


def get_usage_results(
    start_time,
    func_name,
    cpu_usage,
    ram_usage,
    gpu_utilization,
    gpu_memory_usage,
    gpu_name,
):
    time_spent = perf_counter() - start_time
    usage_results = {
        "func_name": func_name,
        "time_spent": time_spent,
    }

    if cpu_usage and ram_usage:
        usage_results["avg_cpu"] = sum(cpu_usage) / len(cpu_usage)
        usage_results["avg_ram"] = sum(ram_usage) / len(ram_usage)
        usage_results["max_cpu"] = max(cpu_usage)
        usage_results["max_ram"] = max(ram_usage)

        usage_results["gpu_name"] = gpu_name
        if gpu_utilization:
            usage_results["avg_gpu_util"] = sum(gpu_utilization) / len(gpu_utilization)
            usage_results["max_gpu_util"] = max(gpu_utilization)
        else:
            usage_results["avg_gpu_util"] = 0
            usage_results["max_gpu_util"] = 0

        if gpu_memory_usage:
            usage_results["avg_gpu_mem"] = sum(gpu_memory_usage) / len(gpu_memory_usage)
            usage_results["max_gpu_mem"] = max(gpu_memory_usage)
        else:
            usage_results["avg_gpu_mem"] = 0
            usage_results["max_gpu_mem"] = 0

    else:
        usage_results["error"] = "Function did not run long enough to collect data."

    return usage_results


def monitor_usage(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        filepath = inspect.getfile(func)
        pid = get_program_pid(
            script_path=filepath,
            filename=os.path.basename(filepath),
        )

        (
            stop_monitoring,
            cpu_usage,
            ram_usage,
            gpu_utilization,
            gpu_memory_usage,
            gpu_name,
        ) = get_program_usage(pid)

        start_time = perf_counter()
        try:
            result = func(*args, **kwargs)

        finally:
            stop_monitoring()
            usage_results = get_usage_results(
                start_time=start_time,
                func_name=func.__name__,
                cpu_usage=cpu_usage,
                ram_usage=ram_usage,
                gpu_utilization=gpu_utilization,
                gpu_memory_usage=gpu_memory_usage,
                gpu_name=gpu_name[0] if len(gpu_name) == 1 else gpu_name,
            )
            print()
            print("***Usage Stats***")
            print(json.dumps(usage_results, indent=4))

        return result

    return wrapper


def time_spent(return_time_spent: bool = False):
    """
    A decorator function to calculate the total time spent by any function to execute.

    ## Usage:
    ```
    @time_spent()
    async def func(*args, **kwargs):
        pass

    ```
    ## Args:
        return_time_spent (bool, optional): If True, returns the measured runtime duration in seconds. Duration is always logged regardless. Defaults to False.
        func (function): The function to be decorated.

    ## Returns:
        function: The decorated function.
    """

    def decorator(func):
        rounding_int = 2
        if asyncio.iscoroutinefunction(func):

            @wraps(func)
            async def wrapper(*args, **kwargs):
                start_time = perf_counter()
                result = await func(*args, **kwargs)
                duration = round(perf_counter() - start_time, rounding_int)
                print(
                    f"INFO: Total Time Taken by function '{func.__name__}': '{duration} s'"
                )
                if return_time_spent:
                    return duration, result

                else:
                    return result

        else:

            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = perf_counter()
                result = func(*args, **kwargs)
                duration = round(perf_counter() - start_time, rounding_int)
                print(
                    f"INFO: Total Time Taken by function '{func.__name__}': '{duration} s'"
                )
                if return_time_spent:
                    return duration, result

                else:
                    return result

        return wrapper

    return decorator


def time_spent_ms(return_time_spent: bool = False):
    """
    A decorator function to calculate the total time spent by any function to execute.

    ## Usage:
    ```
    @time_spent()
    async def func(*args, **kwargs):
        pass

    ```
    ## Args:
        return_time_spent (bool, optional): If True, returns the measured runtime duration in seconds. Duration is always logged regardless. Defaults to False.
        func (function): The function to be decorated.

    ## Returns:
        function: The decorated function.
    """

    def decorator(func):
        rounding_int = 4
        if asyncio.iscoroutinefunction(func):

            @wraps(func)
            async def wrapper(*args, **kwargs):
                start_time = perf_counter()
                result = await func(*args, **kwargs)
                duration = round(perf_counter() - start_time, rounding_int) * 1000
                print(
                    f"INFO: Total Time Taken by function '{func.__name__}': '{duration} ms'"
                )
                if return_time_spent:
                    return duration, result

                else:
                    return result

        else:

            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = perf_counter()
                result = func(*args, **kwargs)
                duration = round(perf_counter() - start_time, rounding_int) * 1000
                print(
                    f"INFO: Total Time Taken by function '{func.__name__}': '{duration} ms'"
                )
                if return_time_spent:
                    return duration, result

                else:
                    return result

        return wrapper

    return decorator
