from random import choice, shuffle

from ..code_dummy import BotActivityDummy
from ...engine.gameobjects.bots.bot_sync import Bot
from ...engine.gameobjects.wall import Wall
from ...engine.utils.direction import Direction
from ...engine.utils.point import Point


class BotActivity:
    def __init__(self, bot: BotActivityDummy):
        self.bot = bot

        self.visited = []

    def perform(self):
        target = self.scan_targets()
        if target:
            self.bot.shoot(target)
            return

        self.bot.step(self.best_direction())

    def scan_targets(self):
        secondary = []
        for obj in self.bot.scan():
            if isinstance(obj, Bot):
                return obj.coord
            elif isinstance(obj, Wall):
                secondary.append(obj.coord)

        return choice(secondary) if len(secondary) > 0 else False

    def check(self, dst: Point) -> bool:
        if 0 <= dst.x < 16 and 0 <= dst.y < 16:
            if not (dst in self.visited):
                return True
        return False

    def best_direction(self) -> Direction:
        directions = Direction.to_list()
        shuffle(directions)
        current = self.bot.current_location()
        for d in directions:
            final = current + d
            if self.check(final):
                self.visited.append(final)
                return d
        return directions[0]
