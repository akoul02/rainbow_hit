from engine.gameobjects.gameobject import GameObject
from dataclasses import dataclass

@dataclass
class Laser(GameObject):
    '''Default weapon.

    Attributes
    ----------
    dest_x : int
        destination x coordinate
    
    dest_y : int
        destination y coordinate

    '''
    dest_x: int
    dest_y: int
