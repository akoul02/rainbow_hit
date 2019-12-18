from typing import Any, List
import time

from collections import deque
from engine.gameobjects.wall import Wall
from engine.gameobjects.destroyable import Destroyable
from engine.gameobjects.bots.enemy_bot import EnemyBot
from engine.gameobjects.bots.bot import Bot
from engine.utils.direction import Direction
from engine.utils.point import Point
from exceptions import *

def continuemain(func):
    '''
    Decorator, that should be added automatically for any user-code
    First argument should be bot instance
    '''
    def wrapper(self, *args, **kwargs):
        try:
            self.main_event.set()

            # block current thread
            self.event.wait()
            self.event.clear()
            ret = func(self, *args, **kwargs)
            return ret
        except (StepsAreOver, ActionsAreOver, BotTimeoutError, BotIsDead) as e:
            # handle ascync-raised exceptions
            return e
        finally:
            # allow main thread to continue
            if isinstance(self, Bot):
                self.main_event.set()
            else:
                raise InvalidSelfInstance('Invalid type of self object!')
    return wrapper

@continuemain
def run_user(bot: Bot):
    pass
    # user code starts here
    # bot.step(Direction.Up)
    # bot.step(Direction.Up)
    # bot.step(Direction.Right)
    # bot.step(Direction.RightUp)
    # bot.step(Direction.Up)
    # for obj in objects:
    #    bot.shoot(obj.coord)

@continuemain
def run_enemy(bot: Bot):
    bot.step(Direction.RightUp)
    bot.step(Direction.Up)
    bot.shoot(Point(4, 4))
    bot.step(Direction.Up)
    bot.step(Direction.Up)
    bot.step(Direction.Up)
    bot.step(Direction.RightUp)
    bot.step(Direction.Up)
    bot.step(Direction.Right)
    bot.step(Direction.Right)
    bot.step(Direction.Right)
    bot.step(Direction.Right)
    bot.step(Direction.Up)
    bot.scan()

@continuemain
def run_enemy2(bot: Bot):
    # bot.step(Direction.DownLeft)
    # bot.step(Direction.DownLeft)
    # bot.step(Direction.DownLeft)
    # bot.step(Direction.DownLeft)
    # bot.step(Direction.Left)
    # bot.step(Direction.RightDown)
    # bot.step(Direction.Left)
    bot.sleep()
    bot.sleep()
    bot.sleep()
    bot.sleep()

@continuemain
def run_enemy3(bot: Bot):
    bot.step(Direction.Up)
    bot.step(Direction.Up)
    objects = bot.scan()
    bot.step(Direction.Up)
    objects = bot.scan()
    bot.step(Direction.Up)
    bot.step(Direction.Up)
    objects = bot.scan()
    bot.step(Direction.Up)
    objects = bot.scan()
    
@continuemain
def run_enemy4(bot: Bot):
    bot.sleep()
    bot.sleep()
    bot.sleep()
    objects = bot.scan()
    bot.sleep()
    bot.sleep()
    
@continuemain
def run_user2(bot: Bot):
    objects = [[0] * 16 for i in range(16)]
    # queue for steps (last 6)
    steps: deque = deque([], 6)

    def at_position(coord: Point) -> bool:
        if objects[coord.x][coord.y]:
            return True
        return False

    def check(world: List[List[int]], dst: Point, current: Point, steps: deque) -> bool:
        if not at_position(current + dst):
            if current.x + dst.x >= 0 and current.x + dst.x < 16 and current.y + dst.y >= 0 and current.y + dst.y < 16:
                if not (current + dst in steps):
                    return True
        return False

    while True:
        for obj in bot.scan():
            if isinstance(obj, Destroyable):
                objects[obj.coord.x][obj.coord.y] = 1

        coord = bot.coord

        direction = Direction.rand_dir()
        while not check(objects, direction.value, coord, steps):
            direction = Direction.rand_dir()

        steps.append(bot.coord)
        bot.step(direction)
