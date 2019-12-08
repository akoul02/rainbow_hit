import unittest

import sys, os
sys.path.insert(0, 'C:\\Users\\madrat\\Desktop\\rainbow_hit\\sources\\server\\game\\')

from engine.utils.point import Point
from engine.gameobjects.game_world import World
from engine.gameobjects.bots.bot import Bot
from engine.utils.direction import Direction

class BotTest(unittest.TestCase):
    def test_stepping(self):
        bot = Bot(Point(0, 0), 10, 10, True, 'test_bot', None, None)

        bot.step(Direction.Up,     blocking=False)
        bot.step(Direction.Up,     blocking=False)
        bot.step(Direction.Up,     blocking=False)
        bot.step(Direction.Left,   blocking=False)
        bot.step(Direction.Left,   blocking=False)
        bot.step(Direction.LeftUp, blocking=False)
        
        self.assertEqual(bot.current_location(), Point(-3, 4))

    def test_shoot(self):
        world = World()
        bot  = Bot(Point(0, 0), 2, 10, True, 'player', None, world)
        bot1 = Bot(Point(1, 1), 1, 10, True, 'player', None, world)
        bot2 = Bot(Point(2, 2), 1, 10, True, 'player', None, world)
        bot3 = Bot(Point(3, 3), 1, 10, True, 'player', None, world)

        objects = bot.scan()
        pass
        

if __name__ == "__main__":
    unittest.main()