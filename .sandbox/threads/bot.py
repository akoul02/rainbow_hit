from dataclasses import dataclass
from threading import Barrier, Thread, Lock
from typing import List
import functools

@dataclass
class Bot:
    x: int
    name: str
    lock: Lock

    def __init__(self, x: int, name: str, lock: Lock):
        self.x = x
        self.name = name
        self.lock = lock
        self.lock.acquire()

    def step(self, n: int):
        self.x += n
        print(f'{self.name} Making {n} steps')
        print(f'{self.name}\'s Current coordinate: {self.x}\n')
        self.lock.acquire()

    def sleep(self):
        print(f'{self.name} is sleeping')
        self.lock.acquire()
