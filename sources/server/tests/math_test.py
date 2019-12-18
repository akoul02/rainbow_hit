import unittest


import sys, os
sys.path.insert(0, os.path.dirname(__file__) + '/../game/')


from engine.utils.point import Point
from engine.gameobjects.game_world import World
from engine.gameobjects.wall import Wall


class MathTest(unittest.TestCase):

    def test_max_hp_over1(self):
        world = World()
        wall = Wall(Point(6, 3), world, 95, 100, True)
        self.assertEqual(wall.increase_health(10), 100)

    def test_max_hp_over2(self):
        world = World()
        wall = Wall(Point(2, 1), world, 30, 100, True)
        self.assertEqual(wall.increase_health(100), 100)

    def test_min_hp_lower1(self):
        world = World()
        wall = Wall(Point(5, 9), world, 35, 100, True)
        self.assertEqual(wall.reduce_health(45), 0)

    def test_min_hp_lower2(self):
        world = World()
        wall = Wall(Point(12, 0), world, 70, 100, True)
        self.assertEqual(wall.reduce_health(100), 0)

    def test_hp_average1(self):
        world = World()
        wall = Wall(Point(4, 4), world, 100, 100, True)
        self.assertEqual(wall.reduce_health(50), 50)

    def test_hp_average2(self):
        world = World()
        wall = Wall(Point(8, 2), world, 100, 100, True)
        self.assertEqual(wall.reduce_health(70), 30)


if __name__ == "__main__":
    unittest.main()