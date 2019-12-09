from __future__ import annotations

from dataclasses import *
from typing import Any, List
import math

from engine.gameobjects.gameobject import GameObject
from engine.gameobjects.destroyable import Destroyable
from engine.utils.point import Point
from engine.gameobjects.bots.user_bot import UserBot
from engine.gameobjects.bots.enemy_bot import EnemyBot
from engine.gameobjects.laser import Laser
from exceptions import GameOver

@dataclass
class World:
    '''Generic world object. It handles all objects inside game world
    Attributes
    ----------
        objects : List[GameObjects]
    '''
    objects: List[GameObject] = field(default_factory=list)
    size_x: int = 16
    size_y: int = 16

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
                    if isinstance(i, UserBot):
                        raise GameOver(False)
                        
                    self.objects.remove(i)
            if isinstance(i, Laser):
                self.objects.remove(i)
        if len([i for i in self.objects if isinstance(i, EnemyBot)]) == 0:
            raise GameOver(True)
                
        return None

    def position(self, coord: Point) -> bool:
        for obj in self.objects:
            if obj.coord == coord:
                return False
        return True
