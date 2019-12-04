from bot import Bot
from typing import Any, List

def run_user(bot: Bot):
    bot.step(1) # user code
    bot.step(3) # user code
    bot.step(5) # user code
    bot.step(7) # user code
    bot.step(8) # user code
    bot.main_event.set()
    # print(actions_are_over[0])
    # raise Bot.ActionsAreOver()        


def run_enemy(bot: Bot):
    bot.step(2)
    bot.step(4)
    bot.step(6)
    bot.main_event.set()
    # print(actions_are_over[0])
    # raise Bot.ActionsAreOver()        

