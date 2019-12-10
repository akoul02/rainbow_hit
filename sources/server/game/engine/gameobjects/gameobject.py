from dataclasses import dataclass

from engine.utils.point import Point
from exceptions import InvalidCoordinate
import engine.gameobjects.game_world as g_world

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
    world: 'g_world.World'

    def __post_init__(self):
        if self.world.at_position(self.coord):
            raise InvalidCoordinate()
        if self.world != None:
            self.world.append(self)

