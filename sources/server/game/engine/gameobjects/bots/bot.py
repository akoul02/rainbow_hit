from dataclasses import dataclass, field
from threading import Event, Timer, Thread
from typing import List, Dict, Any, Callable, Tuple, Union, Optional
from math import pow, sqrt

from exceptions import InvalidSelfInstance, GameException
from constants import *
from engine.utils.direction import Direction
from engine.utils.point import Point
from engine.gameobjects.laser import Laser
from engine.gameobjects.gameobject import GameObject
from engine.gameobjects.destroyable import Destroyable
from engine.utils.math_utils import samelcheck

if IS_DEBUG:
    import threading

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

    last_action: str
        save information about last bot action in serialized (json) format
    '''
    name: str
    main_event: Event
    damage: int = LASER_DAMAGE
    fov: int = BOT_FOV_CELLS
    power_ups: List = field(default_factory=list)
    event: Event = field(default_factory=Event)
    last_action: str = ''

    def synchronized(func: Callable):
        '''Decorator, to synchronize called function with main thread.
        
        First argument should be bot instance. 
        '''
        def wrapper(self, *args: List[Any], **kwargs: Dict[str, Any]):
            flag = kwargs.pop('blocking', True)
            res = func(self, *args, **kwargs)
            if flag:
                if isinstance(self, Bot):
                    # allow main thread to continue execution
                    self.main_event.set()

                    # block current thread
                    self.event.wait()
                    self.event.clear()
                else:
                    raise InvalidSelfInstance()
            return res
        return wrapper

    def serialize(self):
        return f'"({self.coord.x}, {self.coord.y})": ["Bot", "{self.name}", {self.health}, {self.damage}]'

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
        old_coord = Point(self.coord.x, self.coord.y)
        if not self.world.at_position(Point(self.coord.x + dir.value.x, self.coord.y + dir.value.y)):
            if self.coord.x + dir.value.x >= 0 and self.coord.x + dir.value.x < self.world.size_x and self.coord.y + dir.value.y >= 0 and self.coord.y + dir.value.y < self.world.size_y:
                self.coord.x += dir.value.x
                self.coord.y += dir.value.y
        if IS_DEBUG:
            print(f'[{threading.current_thread().name}] {ANSI_CYAN + self.name + ANSI_RES} step: ({old_coord.x}, {old_coord.y}) => ({self.coord.x}, {self.coord.y})')

        self.last_action = STEP_CMD.format(
            self.name, 
            self.coord.x, 
            self.coord.y
        )
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
        if IS_DEBUG:
            print(f'[{threading.current_thread().name}] {ANSI_CYAN + self.name + ANSI_RES} got all coordinates: ')
        objects = [
            obj for obj in self.world.objects
            if self.coord.distance_to(obj.coord) <= self.fov if self != obj
        ]
        if IS_DEBUG:
            for obj in objects:
                print(f'\t{ANSI_GREEN + obj.name + ANSI_RES} : ({obj.coord})')

        return objects
        

    @synchronized
    def shoot(self, obj: Union[Point, GameObject]) -> Optional[int]:
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
        -------
        result : Union[None, int]
            None, if it cant shoot anyone
            int, that represents target health after shot, if it hits successfully
        '''
        if isinstance(obj, Point):
            point = obj
        elif isinstance(obj, GameObject):
            point = obj.coord
        
        class NoneObject:
            def __init__(self, point):
                self.coord = point
                        
        closest = self.world.get_obj_at_position(point)
        if closest == None:
            closest = NoneObject(point)

        _range = lambda x1, x2: range(x1, x2) if x1 != x2 else [x1]

        dbp = lambda x1, y1, x2, y2: sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        heron = lambda a, b, c: sqrt((a+b+c)/2*((a+b+c)/2 - a)*((a+b+c)/2 - b)*((a+b+c)/2 - c))
        a = dbp(point.x, point.y, self.coord.x, self.coord.y)
        dircheck = lambda ox, oy, x1, x2, y1, y2 : True if ox in _range(min(x1, x2), max(x1, x2)) and _range(min(y1, y2), max(y1, y2)) else False
        # samelcheck = lambda ox, oy, x1, x2, y1, y2: True if (ox - x1)/(x2 - x1) == (oy - y1)/(y2 - y1) else False
        for obj in self.world.objects:
            if obj.coord != self.coord and obj != self and self.coord != point and dircheck(obj.coord.x, obj.coord.y, self.coord.x, point.x, self.coord.y, point.y):
                               
                b = dbp(self.coord.x, self.coord.y, obj.coord.x, obj.coord.y)
                c = dbp(point.x, point.y, obj.coord.x, obj.coord.y)
                dist = 2*heron(a, b, c)/a
                if dist <= DELTA or samelcheck(obj.coord.x, obj.coord.y, self.coord.x, point.x, self.coord.y, point.y):
                    if obj.coord.distance_to(self.coord) <= closest.coord.distance_to(self.coord):
                        closest = obj

        res: Optional[int] = 0
        if isinstance(closest, Destroyable):
            l = Laser(self.coord, None, closest.coord, self.damage)
            if IS_DEBUG:
                print(f'[{threading.current_thread().name}] {ANSI_CYAN + self.name + ANSI_RES} shooting at: {closest.coord} [{ANSI_GREEN + self.world.get_obj_at_position(closest.coord).name + ANSI_RES}]')
                print(f'Health after shoot: {self.world.get_obj_at_position(closest.coord).health - self.damage}')
            res = l.shoot(closest)
        else:
            if IS_DEBUG:
                print(f'[{threading.current_thread().name}] {ANSI_CYAN + self.name + ANSI_RES} doesnt found any destroyable objects at {point}')
            res = None

        self.last_action = SHOOT_CMD.format(
            self.name, 
            self.coord.x, 
            self.coord.y, 
            (point.x if type(closest) is NoneObject else closest.coord.x), 
            (point.y if type(closest) is NoneObject else closest.coord.y), 
            ("true" if ((type(closest) is not NoneObject) and not closest.is_alive()) else "false")
        )
        return res

    @synchronized
    def sleep(self) -> None:
        '''Do nothing for 1 step

        Returns
        -------
            None
        '''
        if IS_DEBUG:
            print(f'[{threading.current_thread().name}] {ANSI_CYAN + self.name + ANSI_RES} is sleeping')

        self.last_action = SLEEP_CMD.format(self.name)
        return None
