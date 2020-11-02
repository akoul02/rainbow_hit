from dataclasses import dataclass
from ..utils.point import Point
from ...exceptions import InvalidCoordinate


@dataclass
class GameObject:
    '''Generic class for all game-objects. 
    Any kind of game-objects should be inherited from this class.

    Attributes
    ----------
    coord : Point
        current x and y coordinate
    '''

    coord: Point
    world: object  # 'g_world.World'

    def __post_init__(self):
        if self.world is not None:
            if self.world.at_position(self.coord):
                raise InvalidCoordinate()
            self.world.append(self)
