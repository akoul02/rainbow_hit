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

    def __init__(self, bot: Bot, run_func):
        self.run_func = run_func
        self.bot = bot
        self.thread = Thread(target=self.run_func, args=[self.bot])

    def next_move(self):
        if not self.is_started:
            self.is_started = True
            self.bot.event.set()
            self.thread.start()
        else:
            if self.thread.isAlive():
                self.bot.event.set()
            else:
                self.thread.join()
                raise Bot.ActionsAreOver()