from random import choice

from server.game.bots_code.code_dummy import BotActivityDummy
from server.game.engine.utils.direction import Direction


class BotActivity:
    def __init__(self, bot: BotActivityDummy):
        self.bot = bot

    def perform(self):
        self.bot.step(choice(Direction.to_list()))
