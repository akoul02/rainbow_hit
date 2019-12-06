from engine.gameobjects.gameobject import GameObject
from dataclasses import dataclass

@dataclass
class Bullet(GameObject):
    dest_x: int
    dest_y: int
    speed: int = 10
