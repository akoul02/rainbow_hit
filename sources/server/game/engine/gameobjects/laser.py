from engine.gameobjects.gameobject import GameObject
from dataclasses import dataclass

@dataclass
class Laser(GameObject):
    dest_x: int
    dest_y: int
