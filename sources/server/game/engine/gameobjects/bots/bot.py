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

    fov : int
        Field of view

    power_ups : List[PowerUp]
        All active power ups on bot

    event : Event
        Main syncronise lock for thread with current bot
    '''
    name: str
    main_event: Event
    damage: int = LASER_DAMAGE
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
        '''Get current location as point

        Returns
        -------
        point : Point
            current coordinates
        '''
        return Point(self.coord.x, self.coord.y)
    
    def current_hp(self) -> int:
        '''Get current health

        Returns
        -------
        health : int
            Current health
        '''
        return self.health
    
    def scan(self) -> List[GameObject]:
        '''Find objects around you in world

        Iterate throught all objects inside world, 
        and return objects, that are inside players FOV 

        Returns
        -------
        objects : List[GameObject]
            Objects, that are inside players FOV
        '''
        return [
            obj for obj in self.world.objects
            if self.coord.distance_to(obj.coord) <= self.fov if self != obj
        ]
    
    @synchronized
    def shoot(self, point: Point) -> Union[None, int]:
        '''Try to shoot using laser at given point

        Function tries to shoot at given point, but before that
        it checks, if there are no more objects on a line between player
        and target. If it founds object between, it will shoot him. 
        (see ./diagrams/graph.jpg )

        Parameters
        ----------
        point : Point
            point, where you want to shoot
        
        Returns
        result : Union[None, int]
            None, if it cant shoot anyone
            int, that represents target health after shot, if it hits successfully
        -------
        '''
        k1 = (self.coord.y - point.y) / (self.coord.x - point.x)
        b1 = self.coord.y - self.coord.x * k1
        y1 = lambda x: k1 * x + b1
        
        closest = GameObject(Point(MAX_COORD, MAX_COORD), None)
        for obj in self.world.objects:
            if obj != self:
                k2 = (self.coord.y - obj.coord.y) / (self.coord.x - obj.coord.x)
                b2 = self.coord.y - self.coord.x * k2
                y2 = lambda x: k2 * x + b2

                if abs(y1(obj.coord.x) - y2(obj.coord.x)) <= DELTA:
                    if obj.coord.distance_to(self.coord) <= closest.coord.distance_to(self.coord):
                        closest = obj
        
        if not closest.coord == Point(MAX_COORD, MAX_COORD):
            if isinstance(closest, Destroyable):
                l = Laser(self.coord, None, obj.coord, self.damage)
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
