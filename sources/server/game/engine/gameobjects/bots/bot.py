from dataclasses import dataclass, field
from threading import Event, Timer, Thread
from typing import List, Dict, Any, Callable, Tuple
from math import pow, sqrt

from exceptions import InvalidSelfInstance, GameException
from constants import THREAD_TIMEOUT, CELL_SIDE, BOT_FOV_CELLS, BOT_DEFAULT_HP
from engine.utils.direction import Direction
from engine.gameobjects.game_world import World
from engine.gameobjects.gameobject import GameObject
from engine.gameobjects.destroyable import Destroyable

@dataclass
class Bot(Destroyable):
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

    health : ints
        Remaining 'hearts'
    
    power_ups : List[PowerUp]
        All active power ups on bot

    event : Event
        Main syncronise lock for thread with current bot
    '''
    name: str
    main_event: Event
    world: World
    fov: int = BOT_FOV_CELLS
    power_ups: List = field(default_factory=list)
    event: Event = field(default_factory=Event)

    def synchronized(func: Callable):
        '''Decorator, to syncronise called function with main thread.
        
        First argument should be bot instance. 
        '''
        def wrapper(self, *args: List[Any], **kwargs: Dict[str, Any]):
            if kwargs.pop('blocking', True):
                if isinstance(self, Bot):
                    # allow main thread to continue execution
                    self.main_event.set()

                    # block current thread
                    self.event.wait()
                    self.event.clear()
                else:
                    raise exceptions.InvalidSelfInstance('Invalid type of self object!')
            return func(self, *args, **kwargs)
        return wrapper

    @synchronized
    def step(self, dir: Direction) -> Tuple[float, float]:
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

    def current_location(self) -> Tuple[float, float]:
        return (self.x, self.y)
    
    def current_hp(self) -> int:
        return self.health
    
    def scan(self) -> List[GameObject]:
        return [
            obj for obj in self.world
            if sqrt(pow(obj.x - self.x, 2) + pow(obj.y - self.y, 2)) <= self.fov
        ]
    
    @synchronized
    def shoot(self) -> None:
        # TODO
        return None

    @synchronized
    def sleep(self) -> None:
        '''Do nothing for 1 step

        Returns
        -------
            None
        '''
        print(f'{self.name} is sleeping')

        return None
