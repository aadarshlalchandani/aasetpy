## Modify 'src/utils' as per your project
## credits: aadarshlalchandani/aasetpy

from src.utils import inspect, json, os, psutil, threading, time, wraps


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
    stop_monitoring = threading.Event()

    def monitor():
        process = psutil.Process(pid)
        while not stop_monitoring.is_set():
            try:
                cpu_usage.append(process.cpu_percent(interval=interval))
                ram_usage.append(process.memory_percent())
            except KeyboardInterrupt:
                break
            except psutil.NoSuchProcess:
                break
            time.sleep(interval)

    monitor_thread = threading.Thread(target=monitor)
    monitor_thread.start()

    def stop_monitoring_func():
        stop_monitoring.set()
        monitor_thread.join()

    return stop_monitoring_func, cpu_usage, ram_usage


def get_usage_results(start_time, func_name, cpu_usage, ram_usage):
    end_time = time.time()
    time_spent = end_time - start_time
    usage_results = {
        "func_name": func_name,
        "time_spent": time_spent,
    }
    if cpu_usage and ram_usage:
        usage_results["avg_cpu"] = sum(cpu_usage) / len(cpu_usage)
        usage_results["avg_ram"] = sum(ram_usage) / len(ram_usage)
        usage_results["max_cpu"] = max(cpu_usage)
        usage_results["max_ram"] = max(ram_usage)

    else:
        usage_results["error"] = "Function did not run for enough time to collect data."

    return usage_results


def monitor_usage(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        filepath = inspect.getfile(func)
        pid = get_program_pid(
            script_path=filepath,
            filename=os.path.basename(filepath),
        )
        stop_monitoring, cpu_usage, ram_usage = get_program_usage(pid)

        start_time = time.time()
        try:
            result = func(*args, **kwargs)

        finally:
            stop_monitoring()
            usage_results = get_usage_results(
                start_time=start_time,
                func_name=func.__name__,
                cpu_usage=cpu_usage,
                ram_usage=ram_usage,
            )
            print()
            print("***Usage Stats***")
            print(json.dumps(usage_results, indent=4))

        return result

    return wrapper


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
        print({"time_spent": total_time})

        return result

    return wrapper
