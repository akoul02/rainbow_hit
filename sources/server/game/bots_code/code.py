from typing import Any, List
import time

from engine.gameobjects.bots.bot import Bot
from engine.utils.direction import Direction
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
        except (StepsAreOver, ActionsAreOver, BotTimeoutError):
            # handle ascync-raised exceptions
            return 0
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
    time.sleep(1)
    bot.sleep()
    bot.step(Direction.Up)
    time.sleep(1)
    bot.step(Direction.Up)
    bot.step(Direction.Up)
    time.sleep(0.1)
    bot.step(Direction.Up)
    bot.step(Direction.Up)
    bot.step(Direction.Up)
    time.sleep(0.1)

@continuemain
def run_enemy(bot: Bot):
    bot.step(Direction.Down)
    bot.step(Direction.Down)
    bot.step(Direction.Down)
    time.sleep(0.1)
    bot.step(Direction.Down)
    bot.step(Direction.Down)
    time.sleep(1)

@continuemain
def run_enemy2(bot: Bot):
    time.sleep(0.1)
    bot.step(Direction.Left)
    time.sleep(1)
    bot.step(Direction.Left)
    time.sleep(0.01)
    bot.step(Direction.Left)
    time.sleep(0.1)

    # emulate situation, where thread hangs
    while True:
       pass
    
