from dataclasses import dataclass

from engine.gameobjects.gameobject import GameObject

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
    damage: int
