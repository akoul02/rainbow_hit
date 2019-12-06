from dataclasses import dataclass
from threading import Event, Timer, Thread
from typing import List
from exceptions import InvalidSelfInstance, GameException
from constants import THREAD_TIMEOUT

from engine.gameobjects.gameobject import GameObject

@dataclass
class Bot(GameObject):
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

    def synchronized(func):
        '''
        Decorator, to syncronise called function with main thread.
        First argument should be bot instance. 
        '''
        def wrapper(*args, **kwargs):
            if kwargs.pop('blocking', True):
                if isinstance(args[0], Bot):
                    # allow main thread to continue execution
                    args[0].main_event.set()

                    # block current thread
                    args[0].event.wait()
                    args[0].event.clear()
                else:
                    raise exceptions.InvalidSelfInstance('Invalid type of self object!')
            return func(*args, **kwargs)
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

    @synchronized
    def step(self, n: int, *args, **kwargs):
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

    @synchronized
    def sleep(self, *args, **kwargs):
        '''Do nothing for 1 step

        Returns
        -------
            None
        '''
        print(f'{self.name} is sleeping')

        return None