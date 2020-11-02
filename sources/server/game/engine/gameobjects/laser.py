from dataclasses import dataclass
from .gameobject import GameObject
from .destroyable import Destroyable
from ..utils.point import Point


@dataclass
class Laser(GameObject):
    '''Default weapon.

    Attributes
    ----------
    dst_point : Point
        destination x and y coordinate
    '''
    dst_point: Point
    damage: int

    def shoot(self, obj: Destroyable):
        obj.reduce_health(self.damage)
        if obj.health == 0:
            obj.kill()

        return obj.health
