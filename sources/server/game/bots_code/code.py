from typing import Any, List
import time

from engine.gameobjects.bots.bot import Bot
from engine.utils.direction import Direction
import exceptions

def continuemain(func):
    '''
    Decorator, that should be added automatically for any user-code
    First argument should be bot instance
    '''
    def wrapper(self, *args, **kwargs):
        ret = func(self, *args, **kwargs)
        if isinstance(self, Bot):
            self.main_event.set()
        else:
            raise exceptions.InvalidSelfInstance('Invalid type of self object!')
        return ret
    return wrapper

@continuemain
def run_user(bot: Bot):
    # user code starts here
    bot.step(Direction.Up)
    bot.step(Direction.Up)
    bot.sleep()
    bot.step(Direction.Up)

@continuemain
def run_enemy(bot: Bot):
    bot.step(Direction.Down)
    bot.step(Direction.Down)
    bot.step(Direction.Down)

@continuemain
def run_enemy2(bot: Bot):
    def step_more(n: int):
        for i in range(n):
            bot.step(Direction.Left)
    step_more(2)
    # TODO: if thread hangs kill it
    # while True:
    #    pass
    # step_more(5)
    
