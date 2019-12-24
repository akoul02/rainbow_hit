from typing import Any, List
import time

from collections import deque
from engine.gameobjects.wall import Wall
from engine.gameobjects.destroyable import Destroyable
from engine.gameobjects.bots.user_bot import UserBot
from engine.gameobjects.bots.bot import Bot
from engine.utils.direction import Direction
from engine.utils.point import Point
from exceptions import *
import random

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
def run_user1(bot: Bot):
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
                   
@continuemain
def run_user2(bot: Bot):
    objects = [[False] * 16 for i in range(16)]
    '''
    This algorithm performs the following sequence of actions:
    1. Generates a random direction of movement on the map;
    2. Checks the ability to take a step to this point;
    3. Executes step;
    4. Performs an enemy check:
    If it's a bot, makes a shot.
     '''
    # queue for steps (last 6)
    steps: deque = deque([], 20)
    step_directions: deque = deque([], 20)

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