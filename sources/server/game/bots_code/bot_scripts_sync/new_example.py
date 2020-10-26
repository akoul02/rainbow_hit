from random import choice

from server.game.engine.utils.direction import Direction


class BotActivity:
    def __init__(self, bot: object):
        self.bot = bot

    def perform(self):
        self.bot.step(choice(Direction.to_list()))
