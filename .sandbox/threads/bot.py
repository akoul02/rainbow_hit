from dataclasses import dataclass
from threading import Barrier, Thread, Lock, Event
from typing import List
import exceptions

@dataclass
class Bot:
    x: int
    name: str
    event: Event

    class ActionsAreOver(exceptions.GameException):
        def __init__(self):
            exceptions.GameException.__init__(self, 'Bot actions are over!')

    def syncronised(func):
        def wrapper(*args, **kwargs):
            ret = func(*args, **kwargs)
            if isinstance(args[0], Bot):
                args[0].main_event.set()

                args[0].event.wait()
                args[0].event.clear()
            else:
                raise exceptions.InvalidSelfInstance()
            return ret
        return wrapper

    def __init__(self, x: int, name: str, main_event: Event):
        self.x = x
        self.name = name
        self.event = Event()
        self.main_event = main_event

    @syncronised
    def step(self, n: int):
        self.x += n
        print(f'{self.name} Making {n} steps')
        print(f'{self.name}\'s Current coordinate: {self.x}\n')

        return n

    @syncronised
    def sleep(self):
        print(f'{self.name} is sleeping')

        return None

