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
            return 0
        finally:
            if isinstance(self, Bot):
                self.main_event.set()
            else:
                raise InvalidSelfInstance('Invalid type of self object!')
    return wrapper

@continuemain
def run_user(bot: Bot):
    # user code starts here
    bot.sleep()
    bot.step(Direction.Up)
    bot.step(Direction.Up)
    bot.step(Direction.Up)
    bot.step(Direction.Up)

@continuemain
def run_enemy(bot: Bot):
    bot.step(Direction.Down)
    bot.step(Direction.Down)
    bot.step(Direction.Down)
    bot.step(Direction.Down)
    bot.step(Direction.Down)

@continuemain
def run_enemy2(bot: Bot):
    bot.step(Direction.Left)
    bot.step(Direction.Left)
    bot.step(Direction.Left)
    while True:
       pass
    step_more(5)
    
