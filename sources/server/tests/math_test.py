import unittest


import sys, os
sys.path.insert(0, os.path.dirname(__file__) + '/../game/')


from engine.utils.point import Point
from engine.gameobjects.game_world import World
from engine.gameobjects.wall import Wall


class MathTest(unittest.TestCase):

    def test_max_hp_over(self):
        world = World()
        wall = Wall(Point(0, 0), world, 95, 100, True)
        self.assertEqual(wall.increase_health(10), 100)

    def test_min_hp_lower(self):
        world = World()
        wall = Wall(Point(0, 0), world, 35, 100, True)
        self.assertEqual(wall.reduce_health(45), 0)

    def test_hp_average(self):
        world = World()
        wall = Wall(Point(4, 4), world, 100, 100, True)
        self.assertEqual(wall.reduce_health(50), 50)



if __name__ == "__main__":
    unittest.main()