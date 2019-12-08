from __future__ import annotations

from dataclasses import *
from typing import Any, List
import math

from engine.gameobjects.gameobject import GameObject
from engine.gameobjects.destroyable import Destroyable
from engine.gameobjects.laser import Laser

@dataclass
class World:
    '''Generic world object. It handles all objects inside game world
    Attributes
    ----------
        objects : List[GameObjects]
    '''
    objects: List[GameObject] = field(default_factory=list)

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

    # TODO
    @staticmethod
    def generate() -> World:
        '''Creates new instance of World object, with generated map
        '''
        return World()

    def update(self) -> None:
        '''Update state of game world.

        Iterate trough all objects inside world, and delete them, if necessery
        '''
        for i in self.objects:
            if isinstance(i, Destroyable):
                if not i.alive:
                    self.objects.remove(i)
            if isinstance(i, Laser):
                self.objects.remove(i)
        return None
