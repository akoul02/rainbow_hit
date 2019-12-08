from dataclasses import dataclass, field
from threading import Event, Timer, Thread
from typing import List, Dict, Any, Callable, Tuple, Union
from math import pow, sqrt

from exceptions import InvalidSelfInstance, GameException
from constants import *
from engine.utils.direction import Direction
from engine.utils.point import Point
from engine.gameobjects.laser import Laser
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

    world : World
        Reference to a world

    fov : int
        Field of view

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

    # add current bot to game world
    def __post_init__(self):
        if self.world != None:
            self.world.append(self)

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
                    raise InvalidSelfInstance()
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
        point : Point
            current player x and y coordinate
        '''
        
        self.coord.x += dir.get_coords().x
        self.coord.y += dir.get_coords().y

        print(f'{self.name}\'s current coordinate: ({self.coord.x}, {self.coord.y})')

        return Point(self.coord.x, self.coord.y)

    def current_location(self) -> Point:
        return Point(self.coord.x, self.coord.y)
    
    def current_hp(self) -> int:
        return self.health
    
    def scan(self) -> List[GameObject]:
        return [
            obj for obj in self.world
            if self.coord.distance_to(obj.coord) <= self.fov
        ]
    
    @synchronized
    def shoot(self, point: Point) -> Union[None, int]:
        # y = kx + b
        k1 = (self.coord.y - point.y) / (self.coord.x - point.x)
        b1 = self.coord.y - self.coord.x * k1
        # find graph for default point
        y1 = lambda x: k1 * x + b1
        
        closest = GameObject(Point(MAX_COORD, MAX_COORD))
        for obj in self.world:
            k2 = (self.coord.y - obj.coord.y) / (self.coord.x - obj.coord.x)
            b2 = self.coord.y - self.coord.x * k2

            y2 = lambda x: k2 * x + b2

            if abs(y1(obj.coord.x) - y2(obj.coord.x)) <= DELTA:
                if obj.distance_to(self.coord) <= closest.distance_to(self.coord):
                    closest = obj
        
        if not closest.coord == Point(MAX_COORD, MAX_COORD):
            if isinstance(closest, Destroyable):
                l = Laser(obj.coord, LASER_DAMAGE)
                return l.shoot(closest)

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
