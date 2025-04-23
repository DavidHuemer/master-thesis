import concurrent.futures
import multiprocessing


def longer_task(x):
    raise Exception("TEST")
    return f"Task {x} completed"


def task_wrapper(x, q):
    try:
        result = longer_task(x)
        q.put(result)
    except Exception as e:
        q.put(e)


def run_process(x):
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=task_wrapper, args=(x, q))
    p.start()
    p.join(2)  # timeout after 5 seconds

    if p.is_alive():
        p.terminate()
        p.join()
        return f"Task {x} timed out"

    result = q.get()
    if isinstance(result, Exception):
        raise result
    return result


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")  # Needed for Windows compatibility
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(run_process, range(100)))

    print(results)
