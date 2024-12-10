import multiprocessing
import threading
import sys
import queue
import time
import codecs
import os

def print_timing(*args):
    print(f"[{time.asctime()}]", *args)

def send_to_rot(stop, local_queue: queue.Queue, out_queue: multiprocessing.Queue):
    last_send_ts = 0
    while stop.is_set() == False:
        try:
            lowerString = local_queue.get(timeout=0.01)
            now = time.time()
            if now - last_send_ts < 5:
                time.sleep(5 - now + last_send_ts)

            out_queue.put(lowerString)
            last_send_ts = time.time()

        except:
            pass

def lower_start(stop, in_queue: multiprocessing.Queue, out_queue: multiprocessing.Queue):
    print_timing(f"Process A(pid={os.getpid()}) started")

    local_queue = queue.Queue()

    send_to_rot_thread = threading.Thread(target=send_to_rot, args=(stop, local_queue, out_queue))
    send_to_rot_thread.start()

    while stop.is_set() == False:
        try:
            line = in_queue.get(timeout=0.01)
            print_timing(f"Process A(pid={os.getpid()}): got '{ line }'")
            local_queue.put(line.lower())
        except:
            pass
    
    send_to_rot_thread.join()
    
    print_timing(f"Process A(pid={os.getpid()}) exited")

def rotter_start(stop, in_queue: multiprocessing.Queue, out_queue: multiprocessing.Queue):
    print_timing(f"Process B(pid={os.getpid()}) started")

    while stop.is_set() == False:
        try:
            lower_string = in_queue.get(timeout=0.01)
            result = codecs.encode(lower_string, 'rot_13')
            print_timing(f"Process B(pid={os.getpid()}): '{lower_string}' -> '{result}'")
            out_queue.put(result)
        except:
            pass

    print_timing(f"Process B(pid={os.getpid()}) exited")

def main():
    print_timing(f"Main process(pid={os.getpid()}) started")

    stop_event = multiprocessing.Event()
    
    main_lower_queue = multiprocessing.Queue()
    lower_rotter_queue = multiprocessing.Queue()
    lower_process = multiprocessing.Process(target=lower_start, args=(stop_event, main_lower_queue, lower_rotter_queue), daemon=True)
    lower_process.start()

    main_rotter_queue = multiprocessing.Queue()
    rotterProcess = multiprocessing.Process(target=rotter_start, args=(stop_event, lower_rotter_queue, main_rotter_queue), daemon=True)
    rotterProcess.start()

    stop_if_null = threading.Event()
    counter_lock = threading.Lock()
    counter = 0

    def get_results():
        while True:
            nonlocal counter

            with counter_lock:
                if stop_if_null.is_set() and counter == 0:
                    return
            try:
                answer = main_rotter_queue.get(timeout=0.01)
                with counter_lock:
                    counter -= 1
                print_timing(f"Main process(pid={os.getpid()}): got answer '{ answer }'")
            except:
                pass

    recieve_thread = threading.Thread(target=get_results)
    recieve_thread.start()

    for line in sys.stdin:
        main_lower_queue.put(line.rstrip())
        with counter_lock:
            counter += 1
    stop_if_null.set()

    recieve_thread.join()
    stop_event.set()

    lower_process.join()
    rotterProcess.join()

    print_timing(f"Main process(pid={os.getpid()}) exited")        

if __name__ == "__main__":
    main()
