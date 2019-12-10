import unittest

import sys, os
sys.path.insert(0, os.path.dirname(__file__) + '/../game/')

from engine.utils.point import Point
from engine.gameobjects.game_world import World
from engine.gameobjects.bots.bot import Bot
from engine.gameobjects.wall import Wall
from engine.utils.direction import Direction

class BotTest(unittest.TestCase):
    def test_stepping(self):
        bot = Bot(Point(0, 0), None, 10, 10, True, 'test_bot', None)

        bot.step(Direction.Up,     blocking=False)
        bot.step(Direction.Up,     blocking=False)
        bot.step(Direction.Up,     blocking=False)
        bot.step(Direction.Left,   blocking=False)
        bot.step(Direction.Left,   blocking=False)
        bot.step(Direction.LeftUp, blocking=False)
        
        self.assertEqual(bot.current_location(), Point(-3, 4))

    def test_scan(self):
        world = World()
        bot  = Bot(Point(0, 0), world, 2, 10, True, 'player', None)
        bot1 = Bot(Point(1, 1), world, 1, 10, True, 'player', None)
        bot2 = Bot(Point(2, 2), world, 1, 10, True, 'player', None)
        bot3 = Bot(Point(3, 3), world, 1, 10, True, 'player', None)

        objects = bot.scan()
        self.assertEqual(len(objects), 3)
        
    def test_shoot1(self):
        world = World()
        bot  = Bot(Point(0, 0), world, 2, 10, True, 'player', None)
        bot1 = Bot(Point(1, 1), world, 1, 10, True, 'enemy1', None)
        bot2 = Bot(Point(2, 2), world, 1, 10, True, 'enemy2', None,)
        bot3 = Bot(Point(3, 3), world, 1, 10, True, 'enemy3', None)

        bot.shoot(Point(3, 3), blocking=False)
        world.update()
        bot.shoot(Point(3, 3), blocking=False)
        world.update()
        bot.shoot(Point(3, 3), blocking=False)
        world.update()

        self.assertEqual(len(world.objects), 1)

    def test_shoot2(self):
        world = World()
        bot  = Bot(Point(0, 0), world, 2, 10, True, 'player', None)
        bot1 = Bot(Point(3, 1), world, 1, 10, True, 'enemy1', None)
        bot2 = Bot(Point(4, 2), world, 1, 10, True, 'enemy2', None)

        bot.shoot(Point(4, 2), blocking=False)
        world.update()
        self.assertEqual(bot1.is_alive(), False)
        
        bot.shoot(Point(4, 2), blocking=False)
        world.update()
        self.assertEqual(bot2.is_alive(), False)

        self.assertEqual(len(world.objects), 1)

    def test_shoot3(self):
        world = World()
        bot  = Bot(Point(0, 0), world, 2, 10, True, 'player', None)
        wall = Wall(Point(2, 2), world, 1, 1, True)
        bot1 = Bot(Point(3, 3), world, 1, 10, True, 'enemy1', None)

        bot.shoot(Point(3, 3), blocking=False)
        world.update()
        self.assertEqual(wall.is_alive(), False)
        self.assertEqual(bot.is_alive(), True)

        bot.shoot(Point(3, 3), blocking=False)
        world.update()
        self.assertEqual(bot1.is_alive(), False)


if __name__ == "__main__":
    unittest.main()
