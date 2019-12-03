from bot import Bot
from typing import Any, List

def run_user(bot: Bot, actions_are_over: List[bool]):
    bot.step(1) # user code
    bot.step(3) # user code
    bot.step(5) # user code
    actions_are_over[0] = True # <- must be added automatically
    print(actions_are_over[0])
    raise Bot.ActionsAreOver()        


def run_enemy(bot: Bot, actions_are_over: List[bool]):
    bot.step(2)
    bot.step(4)
    bot.step(6)
    actions_are_over[0] = True
    print(actions_are_over[0])
    raise Bot.ActionsAreOver()        

