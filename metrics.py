import time

def runtime_metrics(func):
    start_time = time.perf_counter()
    func()
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Elapsed Time: {elapsed_time:.6f} seconds.")