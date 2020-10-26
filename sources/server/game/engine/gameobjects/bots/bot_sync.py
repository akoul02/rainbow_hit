from dataclasses import dataclass, field
from math import sqrt
from typing import List, Dict, Any, Callable, Tuple, Union, Optional

from server.game.constants import *
from server.game.engine.utils.direction import Direction
from server.game.engine.utils.point import Point
from server.game.engine.gameobjects.laser import Laser
from server.game.engine.gameobjects.gameobject import GameObject
from server.game.engine.gameobjects.destroyable import Destroyable

from server.game.exceptions import InvalidSelfInstance


@dataclass
class Bot(Destroyable):
    name: str
    damage: int = LASER_DAMAGE
    fov: int = BOT_FOV_CELLS
    power_ups: List = field(default_factory=list)
    last_action: str = ''

    def serialize(self):
        return f'"({self.coord.x}, {self.coord.y})": ["Bot", "{self.name}", {self.health}, {self.damage}]'

    def step(self, dir: Direction):
        old_coord = Point(self.coord.x, self.coord.y)
        if not self.world.at_position(Point(self.coord.x + dir.x, self.coord.y + dir.y)):
            if self.coord.x + dir.x >= 0 and self.coord.x + dir.x < self.world.size_x and self.coord.y + dir.y >= 0 and self.coord.y + dir.y < self.world.size_y:
                self.coord.x += dir.x
                self.coord.y += dir.y

        ret = STEP_CMD.format(
            self.name,
            self.coord.x,
            self.coord.y
        )
        return ret

    def current_location(self) -> Point:
        return Point(self.coord.x, self.coord.y)

    def current_hp(self) -> int:
        return self.health

    def scan(self) -> List[GameObject]:
        objects = [
            obj for obj in self.world.objects
            if self.coord.distance_to(obj.coord) <= self.fov if self != obj
        ]

        return objects

    def shoot(self, obj: Union[Point, GameObject]) -> Optional[int]:
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
        heron = lambda a, b, c: sqrt(
            (a + b + c) / 2 * ((a + b + c) / 2 - a) * ((a + b + c) / 2 - b) * ((a + b + c) / 2 - c))
        a = dbp(point.x, point.y, self.coord.x, self.coord.y)
        dircheck = lambda ox, oy, x1, x2, y1, y2: True if ox in _range(min(x1, x2), max(x1, x2)) and oy in _range(
            min(y1, y2), max(y1, y2)) else False
        for obj in self.world.objects:
            dch = dircheck(obj.coord.x, obj.coord.y, self.coord.x, point.x, self.coord.y, point.y)
            if obj.coord != self.coord and obj != self and self.coord != point and dircheck(obj.coord.x, obj.coord.y,
                                                                                            self.coord.x, point.x,
                                                                                            self.coord.y, point.y):
                b = dbp(self.coord.x, self.coord.y, obj.coord.x, obj.coord.y)
                c = dbp(point.x, point.y, obj.coord.x, obj.coord.y)
                dist = 2 * heron(a, b, c) / a
                if dist <= DELTA:
                    if obj.coord.distance_to(self.coord) <= closest.coord.distance_to(self.coord):
                        closest = obj

        res: Optional[int] = 0
        if isinstance(closest, Destroyable):
            l = Laser(self.coord, None, closest.coord, self.damage)
            res = l.shoot(closest)
        else:
            res = None

        ret = SHOOT_CMD.format(
            self.name,
            self.coord.x,
            self.coord.y,
            (point.x if type(closest) is NoneObject else closest.coord.x),
            (point.y if type(closest) is NoneObject else closest.coord.y),
            ("true" if ((type(closest) is not NoneObject) and not closest.is_alive()) else "false")
        )
        return ret

    def sleep(self) -> None:
        return SLEEP_CMD.format(self.name)
