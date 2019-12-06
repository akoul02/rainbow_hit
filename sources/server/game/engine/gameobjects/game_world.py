from dataclasses import *
from typing import Any
import math

from engine.gameobjects.gameobject import GameObject

@dataclass
class World():
    '''Generic world object. It handles all objects inside game world
    Attributes
    ----------
        objects : List[GameObjects]
    '''
    objects: list = field(default_factory=list)

    def append(self, obj: GameObject) -> list:
        '''Appends new object to world 

        Parameters
        ----------
        obj : GameObject
            Any kind of game object

        Returns
        -------
        objects : list
            all game-objects
        '''
        self.objects.append(obj)
        return self.objects
