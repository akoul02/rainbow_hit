from __future__ import annotations

import math
import random
from dataclasses import *
from typing import Any, List

from engine.gameobjects.wall import Wall
from engine.gameobjects.gameobject import GameObject
from engine.gameobjects.destroyable import Destroyable
from engine.utils.point import Point
from engine.gameobjects.bots.user_bot import UserBot
from engine.gameobjects.bots.bot import Bot
from engine.gameobjects.bots.enemy_bot import EnemyBot
from engine.gameobjects.laser import Laser
from exceptions import GameOver
from constants import *

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


    def draw(self):
        print('┌' + '─' * self.size_y * 2+ '┐')
        for i in range(self.size_x - 1, -1, -1):
            s = '│'
            for j in range(self.size_y):
                obj = self.get_obj_at_position(Point(j, i))
                if isinstance(obj, Wall):
                    s += '■■'
                elif isinstance(obj, UserBot):
                    s += '♖ '
                else:
                    s += '  ' # ░░
            s += '│'
            print(s)
        print('└' + '─' * self.size_y * 2 + '┘')

    @staticmethod
    def generate(mode: str, maze_density=3, x_size=FIELD_X, y_size=FIELD_Y) -> World:
        '''Creates new instance of World object, with generated map

        Parameters
        ----------
        mode : str
            pve/pvp/pvpve
        '''

        def removeWall(cf, cs, m):
            x = (cf[0] - cs[0]) // 2
            y = (cf[1] - cs[1]) // 2
            m[cs[0] + x][cs[1] + y] = 0

        def getNeighbours(mh, mw, cell, m):
            res = []
            x = cell[0]
            y = cell[1]

            if (y + 2) < mw and m[x][y + 2][-1] != 1:  # right
                res.append(m[x][y + 2])

            if (x + 2) < mh and m[x + 2][y][-1] != 1:  # down
                res.append(m[x + 2][y])

            if (y - 2) > 0 and m[x][y - 2][-1] != 1:  # left
                res.append(m[x][y - 2])

            if (x - 2) > 0 and m[x - 2][y][-1] != 1:  # up
                res.append(m[x - 2][y])

            return res

        w0 = x_size
        h0 = y_size
        w = 2 * w0 + 1
        h = 2 * h0 + 1
        maze: List[List[int]] = []
        stackcurr = []
        unvisitedcells = w0 * h0

        for i in range(h):
            maze.append([])

            if (i % 2 == 0):
                maze[i].extend([int(x) for x in '1' * w])

            else:
                for j in range(w):

                    if (j % 2 == 0):
                        maze[i].append(1)

                    else:
                        maze[i].append([i, j, 0])

        startcell = random.randrange(1, h, 2)
        currentcell = maze[startcell][1]
        maze[startcell][0] = 0
        currentcell[-1] = 1
        unvisitedcells -= 1
        stackcurr.append(currentcell)

        while (unvisitedcells):
            neigh = getNeighbours(h, w, currentcell, maze)

            if (neigh):
                randnum = random.randint(0, len(neigh) - 1)
                neighbourcell = neigh[randnum]
                neighbourcell[-1] = 1
                unvisitedcells -= 1
                removeWall(neighbourcell, currentcell, maze)
                currentcell = neighbourcell
                stackcurr.append(neighbourcell)

            else:
                stackcurr.pop()
                currentcell = stackcurr[-1]

        endcell = random.randrange(1, h, 2)
        maze[endcell][-1] = 0
        maze_new = []

        for i in range(w0):
            maze_new.append([])

            for j in range(w0):

                if i % 2 == 1:

                    if j % 2 == 1:
                        maze_new[i].append(0)
                        continue
                maze_new[i].append(maze[i][j])

        for i in range(0, len(maze_new)):
            for j in range(0, len(maze_new)):
                if random.randrange(0, 10) < maze_density:
                    maze_new[i][j] = 0 # 1 - maze_new[i][j]

        maze_new[0][0] = 0                      # Empty cell for bot
        maze_new[FIELD_X - 1][FIELD_Y - 1] = 0  # Empty cell for bot

        world = World(mode)
        for i in range(0, len(maze_new)):
            for j in range(0, len(maze_new)):
                if maze_new[i][j]:
                    Wall(Point(i, j), world, 1, 1, True)
                    
        return world

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

