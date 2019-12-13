from typing import Any, List
import time

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
            ret = func(self, *args, **kwargs)
            return ret
        except (StepsAreOver, ActionsAreOver, BotTimeoutError) as e:
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
    # user code starts here
    # bot.step(Direction.Up)
    # bot.step(Direction.Up)
    objects = bot.scan()
    bot.shoot(objects[0].coord)
    bot.step(Direction.Up)
    # for obj in objects:
    #    bot.shoot(obj.coord)


@continuemain
def run_enemy(bot: Bot):
    objects = bot.scan()
    bot.shoot(objects[0].coord)
    bot.sleep()
    bot.sleep()
    bot.sleep()
    bot.sleep()

@continuemain
def run_enemy2(bot: Bot):
    bot.sleep()
    bot.sleep()
    bot.sleep()
    bot.sleep()

@continuemain
def run_enemy3(bot: Bot):
    bot.sleep()
    bot.sleep()
    bot.sleep()
    bot.sleep()
    
@continuemain
def run_enemy4(bot: Bot):
    bot.sleep()
    bot.sleep()
    bot.sleep()
    bot.sleep()
    
