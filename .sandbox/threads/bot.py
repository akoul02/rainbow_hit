from dataclasses import dataclass
from threading import Barrier, Thread, Lock, Event
from typing import List

@dataclass
class Bot:
    x: int
    name: str
    event: Event

    def __init__(self, x: int, name: str, main_event: Event):
        self.x = x
        self.name = name
        self.event = Event()
        self.main_event = main_event

    def step(self, n: int):
        
        self.x += n
        print(f'{self.name} Making {n} steps')
        print(f'{self.name}\'s Current coordinate: {self.x}\n')

        self.main_event.set()
                          # false - wait
        self.event.wait() # true  - continue
        self.event.clear()

        return n

    def sleep(self):

        # self.event.wait()

        print(f'{self.name} is sleeping')

        # self.event.clear()

        return None

