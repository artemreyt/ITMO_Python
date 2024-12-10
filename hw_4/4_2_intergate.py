import math
import time
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def timed(func):
    def inner(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()

        print(f"Execution time of '{func.__name__ : <30}{args + tuple([f'{k}={v}' for k, v in kwargs.items()])}': {end - start:.4f}s")
        return res
    return inner

def integrate_concurrent(f, a, b, *, executor=ThreadPoolExecutor, n_jobs=1, n_iter=10000000):
    step = (b - a) / n_iter
    n_iter_per_task = int(math.ceil(n_iter / n_jobs))

    with executor(max_workers=n_jobs) as e:
        futures = []

        begin, end = 0, n_iter_per_task * step
        iters_done = 0
        for _ in range(n_jobs):
            futures.append(e.submit(integrate, f, begin, end, n_iter=n_iter_per_task))

            iters_done += n_iter_per_task
            begin = end
            end += n_iter_per_task * step
            if end > b:
                end = b
                n_iter_per_task = n_iter - iters_done


        return sum(map(lambda f: f.result(), futures))

def integrate(f, a, b, *, n_iter=10000000):
    print(f'Starting task for {f} on interval [{a}, {b}] with n_iter={n_iter}')
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc

@timed
def multithread_integrate(f, a, b, *, n_jobs=1, n_iter=10000000):
    return integrate_concurrent(f, a, b, n_jobs=n_jobs, executor=ThreadPoolExecutor, n_iter=n_iter)

@timed
def multiprocess_integrate(f, a, b, *, n_jobs=1, n_iter=10000000):
    return integrate_concurrent(f, a, b, n_jobs=n_jobs, executor=ProcessPoolExecutor, n_iter=n_iter)

if __name__ == '__main__':
    precision = 6

    res = round(integrate(math.cos, 0, math.pi / 2), precision)
    print()
    for n in range(1, cpu_count() * 2):
        assert(res == round(multiprocess_integrate(math.cos, 0, math.pi / 2, n_jobs=n), precision))
        print()
        assert(res == round(multithread_integrate(math.cos, 0, math.pi / 2, n_jobs=n), precision))
        print()