from dataclasses import dataclass
from threading import Barrier, Thread, Lock, Event
from typing import List
from exceptions import InvalidSelfInstance, GameException
from time import sleep

@dataclass
class Bot:
    '''Generic class for all bots
    
    All bots are gameobjects. All of their code should be 
    started in separated thread, and managed using "main thread".
    If actions of current bot are over, 'Executor' should raise ActionsAreOver.

    Attributes
    ----------
    x : int
        X-axis coordinate of the bot

    name : str
        Bot handle (simply bot name)

    event : Event
        Main syncronise lock for thread with current bot

    main_event : Event
        Event, to block main thread, until bot finishes his actions
    '''
    x: int
    name: str
    event: Event
    main_event: Event

    class ActionsAreOver(GameException):
        def __init__(self):
            GameException.__init__(self, 'Bot actions are over!')

    def syncronised(func):
        '''
        Simple decorator, to syncronise called function with main thread.
        First argument should be bot instance. 
        '''
        def wrapper(*args, **kwargs):
            if isinstance(args[0], Bot):
                # allow main thread to continue execution
                args[0].main_event.set()

                # block current thread
                args[0].event.wait()
                args[0].event.clear()
            else:
                raise exceptions.InvalidSelfInstance()
            ret = func(*args, **kwargs)
            return ret
        return wrapper

    def __init__(self, x: int, name: str, main_event: Event):
        '''Initializes bot instance

        Parameters
        ----------
        x : int
            initial x-coordinate of the bot

        name : str
            bot name

        main_event:
            Event of the main thread
        '''
        self.x = x
        self.name = name
        self.event = Event()
        self.main_event = main_event

    @syncronised
    def step(self, n: int):
        '''Make n steps

        Parameters
        ----------
        n : int
            number of steps

        Returns
        -------
        self.x : int
            current x-coordinate
        '''
        self.x += n
        print(f'{self.name} making {n} steps')
        print(f'{self.name}\'s current coordinate: {self.x}')

        return self.x

    @syncronised
    def sleep(self):
        '''Do nothing for 1 step

        Returns
        -------
            None
        '''
        print(f'{self.name} is sleeping')

        return None

    def sleep_async(self, n):
        print(f'{self.name} is sleeping for {n} seconds.')
        sleep(n)

        return None

