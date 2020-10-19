import server.game.engine.gameobjects.game_world as g_world
from dataclasses import dataclass
from server.game.engine.utils.point import Point
from server.game.exceptions import InvalidCoordinate


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
        if self.world != None:
            if self.world.at_position(self.coord):
                raise InvalidCoordinate()
            self.world.append(self)
