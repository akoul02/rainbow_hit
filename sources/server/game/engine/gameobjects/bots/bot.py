from dataclasses import dataclass, field
from threading import Event, Timer, Thread
from typing import List, Dict, Any
from exceptions import InvalidSelfInstance, GameException
from constants import THREAD_TIMEOUT, CELL_SIDE, BOT_FOV_CELLS
from utils.direction import Direction
from engine.gameobjects.game_world import World
from math import pow, sqrt

from engine.gameobjects.gameobject import GameObject

@dataclass
class Bot(GameObject):
    '''Generic class for all bots
    
    All bots are gameobjects. All of their code should be 
    started in separated thread, and managed using "main thread".
    If actions of current bot are over, 'Executor' should raise ActionsAreOver.

    Attributes
    ----------
    name : str
        Bot handle (simply bot name)

    main_event : Event
        Event, to block main thread, until bot finishes his actions

    hp : int
        Remaining 'hearts'
    
    boosters : PowerUp
        All active power ups on bot

    event : Event
        Main syncronise lock for thread with current bot
    '''
    name: str
    main_event: Event
    world: World
    hp: int = 10
    fov = BOT_FOV_CELLS
    boosters: List = field(default_factory=list)
    event: Event = field(default_factory=Event)

    def synchronized(func):
        '''Decorator, to syncronise called function with main thread.
        
        First argument should be bot instance. 
        '''
        def wrapper(*args: List[Any], **kwargs: Dict[str, Any]):
            if kwargs.pop('blocking', True):
                if isinstance(args[0], Bot):
                    # sleep(0.01)

                    # allow main thread to continue execution
                    args[0].main_event.set()

                    # block current thread
                    args[0].event.wait()
                    args[0].event.clear()
                else:
                    raise exceptions.InvalidSelfInstance('Invalid type of self object!')
            return func(*args, **kwargs)
        return wrapper

    @synchronized
    def step(self, dir: Direction) -> tuple:
        '''Make 1 step in direction dir

        Parameters
        ----------
        dir : Direction
            direction of a step

        Returns
        -------
        self.x : int
            current x-coordinate
        
        self.y : int
            current y-coordinate
        '''
        
        self.x += dir.get_coords()[0]
        self.y += dir.get_coords()[1]

        print(f'{self.name}\'s current coordinate: ({self.x}, {self.y})')

        return (self.x, self.y)

    def current_location(self) -> tuple:
        return (self.x, self.y)
    
    def current_hp(self) -> int:
        return self.hp
    
    def scan(self) -> list:
        return [obj for obj in self.world if sqrt(pow(self.x, 2) + pow(self.y, 2)) <= self.fov]
    
    @synchronized
    def shoot(self):
        # TBA
        return None

    @synchronized
    def sleep(self):
        '''Do nothing for 1 step

        Returns
        -------
            None
        '''
        print(f'{self.name} is sleeping')

        return None
