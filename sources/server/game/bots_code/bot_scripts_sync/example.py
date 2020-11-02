from random import choice

from ..code_dummy import BotActivityDummy
from ...engine.utils.direction import Direction


class BotActivity:
    def __init__(self, bot: BotActivityDummy):
        self.bot = bot

    def perform(self):
        self.bot.step(choice(Direction.to_list()))
