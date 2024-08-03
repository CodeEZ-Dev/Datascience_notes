### Multithreading
## When to use Multi Threading
###I/O-bound tasks: Tasks that spend more time waiting for I/O operations (e.g., file operations, network requests).
###  Concurrent execution: When you want to improve the throughput of your application by performing multiple operations concurrently.

import threading
import time

def print_numbers():
    for i in range(5):
        time.sleep(2)
        print(f'Numbers: {i}')

def print_letters():
    for letter in "abcde":
        time.sleep(2)
        print(f"letter: {letter}")

##create 2 threads
t1=threading.Thread(target=print_numbers)
t2=threading.Thread(target=print_letters)


start_time = time.time()

## start the thread
t1.start()
t2.start()

### Wait for the threads to complete
t1.join()
t2.join()

end_time = time.time() - start_time
print(end_time)