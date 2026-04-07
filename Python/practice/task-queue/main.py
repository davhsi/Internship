import threading
from queue import Queue # this queue is threadsafe unlike collections.deque. this waits if q.get() is empty
from time import sleep
from random import random

tasks = [
    "system-monitor",
    "memory-monitor",
    "create-new-file",
    "finish-code",
    "system-monitor",
    "memory-monitor",
    "create-new-file",
    "finish-code",
]

q = Queue()


def worker_function():
    while True:
        task = q.get()
        if task["name"] is None:
            q.task_done() # q maintains a counter "unfinished_tasks" this does a -1 to it
            break
        process(task)
        q.task_done()


def handleRetry(task):
    q.put(task) # each put operation increments the "unfinished_task" by 1


def handleFailure(task):
    print(f"{task['name']} failed")


def process(task):
    prob = random() >= 0.5
    if prob:
        print(f"{threading.current_thread().name} is executing {task}")
        sleep(1)
        return
    else:
        task["retries"] += 1
        handleFailure(task) if task["retries"] == 3 else handleRetry(task) # simulating retries


for x in tasks:
    q.put({"name": x, "retries": 0})

# threads = []
for i in range(3):
    th_name = f"thread-{i}"
    t = threading.Thread(target=worker_function, name=th_name)
    t.start()
    # threads.append(t)

q.join() # waits until the attribute "unfinished_tasks" comes down to 0

for _ in range(3):
    q.put({"name": None, "retries": 0})


