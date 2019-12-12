from __future__ import annotations

from dataclasses import *
from typing import Any, List
import math

from engine.gameobjects.gameobject import GameObject
from engine.gameobjects.destroyable import Destroyable
from engine.utils.point import Point
from engine.gameobjects.bots.user_bot import UserBot
from engine.gameobjects.bots.bot import Bot
from engine.gameobjects.bots.enemy_bot import EnemyBot
from engine.gameobjects.laser import Laser
from exceptions import GameOver

@dataclass
class World:
    '''Generic world object. It handles all objects inside game world
    Attributes
    ----------
    game_mode : str
        pvp   - 2 player's fighting against each other (2 UserBot's)
        pvpve - many players + many Enemy bots 
            (win only if anuone is killed expect userbot)
        pve   - 1 player vs bots (1 UserBot, and many EnemyBot's)

    objects : List[GameObjects]
        list with all objects currently presented in game

    size_x : int
        max x-axis size

    size_y : int
        max y-axis size
    '''
    game_mode: str = 'pve'
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
                    self.objects.remove(i)
            if isinstance(i, Laser):
                self.objects.remove(i)
        enemy_objects  = [i for i in self.objects if isinstance(i, EnemyBot)]
        player_objects = [i for i in self.objects if isinstance(i, UserBot)]

        if self.game_mode == 'pvp':
            # there is only one player object
            if len(player_objects) == 1:
                raise GameOver(True, player_objects[0])
            elif len(player_objects) == 0:
                # this should never happen
                raise GameOver(False)
        elif self.game_mode == 'pvpve':
            # TODO
            pass
        elif self.game_mode == 'pve':
            if len(player_objects) == 0:
                raise GameOver(False)
            if len(enemy_objects) == 0:
                raise GameOver(True, player_objects[0])

        return None

    def at_position(self, coord: Point) -> bool:
        for obj in self.objects:
            if obj.coord == coord:
                return True
        return False

    def get_obj_at_position(self, coord: Point) -> GameObject:
        for obj in self.objects:
            if obj.coord == coord:
                return obj
        return None
