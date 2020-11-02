from sources.api import continuemain, Bot, UserBot, Destroyable, Wall, Direction, Point, run, BotActivityDummy
import random
from collections import deque
from typing import Any, List


class BotActivity:
    def __init__(self, bot: BotActivityDummy):
        self.bot = bot

    def perform(self):
        self.bot.step(random.choice(Direction.to_list()))

run(BotActivity)
