import multiprocessing
import multiprocessing.connection
import threading
import time

def fib(n: int):
    if n <= 1:
        return n
    res = 1
    prev = 0
    for i in range(1, n):
        prev, res = res, res + prev

    return res

def timed(func):
    def inner(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()

        print(f"Execution time of '{func.__name__ : <20}{args}': {end - start:.4f}s")
        return res
    return inner

@timed
def multithread_fib(n, n_threads=10):
    threads = []
    results = [None] * n_threads

    def execute(i: int, n: int):
        results[i] = fib(n)

    for i in range(n_threads):
        threads.append(threading.Thread(target=execute, args=(i, n,)))
    
    for t in threads:
        t.start()    
    for t in threads:
        t.join()

    return results


def execute_process(queue: multiprocessing.Queue, func, *args):
    queue.put(func(*args))

@timed
def multiprocess_fib(n, n_processes=10):
    results = [None] * n_processes
    queues = [None] * n_processes
    processes = [None] * n_processes
    for i in range(n_processes):
        queues[i] = multiprocessing.Queue()
        processes[i] = multiprocessing.Process(target=execute_process, args=(queues[i], fib, n))
    
    for p in processes:
        p.start()
    for i, p in enumerate(processes):
        res = queues[i].get()
        results[i] = res
    return results

@timed
def conseq_fib(n: int, times=10):
    results = []
    for _ in range(times):
        results.append(fib(n))
    return results


def test(n: int, times=10):
    res = conseq_fib(n, times)
    assert(res == multithread_fib(n, times))
    assert(res == multiprocess_fib(n, times))

if __name__ == "__main__":
    for power in range(1, 7):
        test(10 ** power)
        print()
