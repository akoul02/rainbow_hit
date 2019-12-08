from dataclasses import dataclass
from engine.utils.math_utils import clamp

from engine.gameobjects.gameobject import GameObject

@dataclass
class Destroyable(GameObject):
    health: int
    max_health: int
    alive: bool

    def reduce_health(self, n: int) -> int:
        self.health = clamp(self.health - n, 0, self.max_health)
        return self.health
    
    def increase_health(self, n: int) -> int:
        self.health = clamp(self.health + n, 0, self.max_health)
        return self.health
    
    def is_alive(self) -> bool:
        return self.alive
    
    def kill(self) -> None:
        self.health = 0
        self.alive = False
        return None
