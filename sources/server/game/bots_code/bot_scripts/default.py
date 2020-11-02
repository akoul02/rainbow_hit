import random
import time
from collections import deque
from ..code import continuemain
from ...engine.gameobjects.bots.bot import Bot
from ...engine.gameobjects.bots.user_bot import UserBot
from ...engine.gameobjects.destroyable import Destroyable
from ...engine.gameobjects.wall import Wall
from ...engine.utils.direction import Direction
from ...engine.utils.point import Point
from ...exceptions import *
from typing import Any, List


@continuemain
def perform(bot: Bot):
    objects = [[False] * 16 for i in range(16)]
    # queue for steps (last 6)
    steps: deque = deque([], 10)
    step_directions: deque = deque([], 10)

    def at_position(world: List[List[bool]], coord: Point) -> bool:
        if world[coord.x][coord.y]:
            return True
        return False

    def check(world: List[List[bool]], dst: Point, current: Point, steps: deque) -> bool:
        if current.x + dst.x >= 0 and current.x + dst.x < 16 and current.y + dst.y >= 0 and current.y + dst.y < 16:
            if not at_position(world, current + dst):
                if not (current + dst in steps):
                    return True
        return False

    clean_directions = list(Direction)

    while True:
        for obj in bot.scan():
            if isinstance(obj, Wall):
                objects[obj.coord.x][obj.coord.y] = True

        shooted = False
        for obj in bot.scan():
            if isinstance(obj, UserBot):
                bot.shoot(obj)
                shooted = True
                break

        directions = clean_directions.copy()
        random.shuffle(directions)
        if not shooted:
            for idx in range(len(directions)):
                if check(objects, directions[idx].value, bot.coord, steps):
                    steps.append(bot.coord.copy())
                    step_directions.append(directions[idx])
                    bot.step(directions[idx])
                    idx = 0
                    break
                else:
                    continue

            if idx == len(directions) - 1:
                steps.append(bot.coord.copy())
                try:
                    direction = ~step_directions.pop()
                    bot.step(direction)
                except:
                    bot.shoot(bot.scan()[0])
