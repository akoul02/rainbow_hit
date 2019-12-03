from bot import Bot
from threading import Barrier, Thread, Lock, Event
from typing import Any

class Executor:
    bot: Bot
    bot_coord: int
    bot_name: str
    run_func: Any
    thread: Thread

    def __init__(self, bot: Bot, run_func):
        self.run_func = run_func
        self.bot = bot
        self.thread = Thread(target=self.run_func, args=[self.bot])

    def run(self):
        self.thread.start()

    def next_move(self):
        self.bot.event.set()