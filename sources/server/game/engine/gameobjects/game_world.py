from dataclasses import *
from engine.gameobjects.gameobject import GameObject
from engine.gameobjects.bullet import Bullet
import math
from typing import Any

@dataclass
class World():
    objects: list = field(default_factory=list)

    def append(self, obj: Any) -> list:
        self.objects.append(obj)
        return self.objects
