import unittest

import sys, os
sys.path.insert(0, os.path.dirname(__file__) + '/../game/')

from engine.utils.point import Point
from engine.gameobjects.game_world import World
from engine.gameobjects.bots.user_bot import UserBot
from engine.gameobjects.bots.enemy_bot import EnemyBot
from engine.gameobjects.wall import Wall
from engine.utils.direction import Direction
from exceptions import GameOver

class BotTest(unittest.TestCase):
    def test_stepping(self):
        world = World()
        bot = UserBot(Point(0, 0), world, 10, 10, True, 'test_bot', None)

        bot.step(Direction.Up,     blocking=False)
        bot.step(Direction.Up,     blocking=False)
        bot.step(Direction.Up,     blocking=False)
        bot.step(Direction.Right,   blocking=False)
        bot.step(Direction.Right,   blocking=False)
        bot.step(Direction.RightUp, blocking=False)
        
        self.assertEqual(bot.current_location(), Point(3, 4))

    def test_scan(self):
        world = World()
        bot  = UserBot(Point(0, 0), world, 2, 10, True, 'player', None)
        bot1 = UserBot(Point(1, 1), world, 1, 10, True, 'player', None)
        bot2 = UserBot(Point(2, 2), world, 1, 10, True, 'player', None)
        bot3 = UserBot(Point(3, 3), world, 1, 10, True, 'player', None)

        objects = bot.scan()
        self.assertEqual(len(objects), 3)
        
    def test_shoot1(self):
        world = World()
        bot  = UserBot(Point(0, 0), world, 2, 10, True, 'player', None)
        self.assertEqual(bot.is_alive(), True)

        bot1 = EnemyBot(Point(1, 1), world, 1, 10, True, 'enemy1', None)
        self.assertEqual(bot1.is_alive(), True)

        bot2 = EnemyBot(Point(2, 2), world, 1, 10, True, 'enemy2', None)
        self.assertEqual(bot2.is_alive(), True)

        bot3 = EnemyBot(Point(3, 3), world, 1, 10, True, 'enemy3', None)
        self.assertEqual(bot3.is_alive(), True)

        try:
            bot.shoot(Point(3, 3), blocking=False)
            world.update()
            self.assertEqual(bot1.is_alive(), False)

            bot.shoot(Point(3, 3), blocking=False)
            world.update()
            self.assertEqual(bot2.is_alive(), False)

            bot.shoot(Point(3, 3), blocking=False)
            world.update()
            self.assertEqual(bot3.is_alive(), False)
        except GameOver as e:
            self.assertEqual(e.game_won, True)

        self.assertEqual(len(world.objects), 1)

    def test_shoot2(self):
        world = World()
        try:
            bot  = UserBot(Point(0, 0), world, 2, 10, True, 'player', None)
            self.assertEqual(bot.is_alive(), True)

            bot1 = EnemyBot(Point(3, 1), world, 1, 10, True, 'enemy1', None)
            self.assertEqual(bot1.is_alive(), True)
    
            bot2 = EnemyBot(Point(4, 2), world, 1, 10, True, 'enemy2', None)
            self.assertEqual(bot2.is_alive(), True)

            bot.shoot(Point(4, 2), blocking=False)
            world.update()
            self.assertEqual(bot1.is_alive(), False)
            self.assertEqual(bot2.is_alive(), True)
            
            bot.shoot(Point(4, 2), blocking=False)
            world.update()
            self.assertEqual(bot2.is_alive(), False)
        except GameOver as e:
            self.assertEqual(e.game_won, True)

        self.assertEqual(len(world.objects), 1)

    def test_shoot3(self):
        world = World()
        try:
            bot  = UserBot(Point(0, 0), world, 2, 10, True, 'player', None)
            wall = Wall(Point(2, 2), world, 1, 1, True)
            bot1 = EnemyBot(Point(3, 3), world, 1, 10, True, 'enemy1', None)

            bot.shoot(Point(3, 3), blocking=False)
            world.update()
            self.assertEqual(wall.is_alive(), False)
            self.assertEqual(bot.is_alive(), True)

            bot.shoot(Point(3, 3), blocking=False)
            world.update()
        except GameOver:
            pass
        self.assertEqual(bot1.is_alive(), False)

    def test_shoot4(self):
        world = World()
        bot  = UserBot(Point(0, 0), world, 2, 10, True, 'player', None)
        self.assertEqual(bot.is_alive(), True)

        bot1 = EnemyBot(Point(1, 2), world, 1, 10, True, 'enemy1', None)
        self.assertEqual(bot1.is_alive(), True)

        bot2 = EnemyBot(Point(2, 5), world, 1, 10, True, 'enemy1', None)
        self.assertEqual(bot1.is_alive(), True)

        try:
            bot.shoot(Point(2, 5), blocking=False)
            world.update()
            self.assertEqual(bot1.is_alive(), False)
            
            bot.shoot(Point(2, 5), blocking=False)
            world.update()
            self.assertEqual(bot2.is_alive(), False)
        except GameOver as e:
            self.assertEqual(e.game_won, True)

        self.assertEqual(len(world.objects), 1)

    def test_shoot_vertical(self):
        world = World()
        bot  = UserBot(Point(0, 0), world, 2, 10, True, 'player', None)
        self.assertEqual(bot.is_alive(), True)

        bot1 = EnemyBot(Point(2, 2), world, 1, 10, True, 'enemy1', None)
        self.assertEqual(bot1.is_alive(), True)

        bot2 = EnemyBot(Point(4, 4), world, 1, 10, True, 'enemy1', None)
        self.assertEqual(bot1.is_alive(), True)

        try:
            bot.shoot(Point(4, 4), blocking=False)
            world.update()
            self.assertEqual(bot1.is_alive(), False)
            self.assertEqual(bot2.is_alive(), True)
            
            bot.shoot(Point(4, 4), blocking=False)
            world.update()
            self.assertEqual(bot2.is_alive(), False)
        except GameOver as e:
            self.assertEqual(e.game_won, True)

        self.assertEqual(len(world.objects), 1)

if __name__ == "__main__":
    unittest.main()
