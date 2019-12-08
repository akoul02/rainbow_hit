from dataclasses import dataclass

from engine.utils.point import Point

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
