from threading import Barrier, Thread, Lock, Event
from executor import Executor
from typing import List

class Synchroniser:
    threads: List[Thread] = []
    step: int = 0
    
    def __init__(self, executors: List[Executor]):
        for executor in executors:
            self.threads.append(Thread(target=executor.run))
        # self.threads[-1].start()

    def next_move(self):
        if not self.threads[1].is_alive()