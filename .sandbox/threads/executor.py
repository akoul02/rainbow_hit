from bot import Bot
from threading import Barrier, Thread, Lock
from typing import Any

class Executor:
    bot: Bot
    bot_coord: int
    bot_name: str
    code: Any
    lock: Lock

    def __init__(self, bot_coord: int, bot_name: str, lock: Lock, code):
        self.lock = lock
        self.code = code
        self.bot_coord = bot_coord
        self.bot_name  = bot_name

    def init(self):
        self.bot = Bot(self.bot_coord, self.bot_name, self.lock)

    def start(self):
        self.code(bot)
