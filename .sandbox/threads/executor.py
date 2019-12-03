from bot import Bot
from threading import Barrier, Thread, Lock, Event
from typing import Any, List

class Executor:
    bot: Bot
    bot_coord: int
    bot_name: str
    run_func: Any
    thread: Thread
    is_started: bool = False
    is_bot_actions_are_over: List[bool] = [False]

    def __init__(self, bot: Bot, run_func):
        self.run_func = run_func
        self.bot = bot
        self.thread = Thread(target=self.run_func, args=[self.bot, self.is_bot_actions_are_over])

    def next_move(self):
        if not self.is_started:
            self.is_started = True
            # self.bot.event.set()
            self.thread.start()
        else:
            if not self.is_bot_actions_are_over[0]:
                self.bot.event.set()
            else:
                raise Bot.ActionsAreOver()        
                self.thread.join()