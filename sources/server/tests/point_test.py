import unittest

import sys, os
sys.path.insert(0, os.path.dirname(__file__) + '/../game/')

from engine.utils.point import Point

class PointTest(unittest.TestCase):
    def test_distance_to1(self):
        p1 = Point(0, 0)
        p2 = Point(0, 5)

        self.assertEqual(p1.distance_to(p2), 5)

    def test_distance_to2(self):
        p1 = Point(0, 0)
        p2 = Point(3, 4)

        self.assertEqual(p1.distance_to(p2), 5)

    def test_distance1(self):
        p1 = Point(0, 0)
        p2 = Point(3, 4)

        self.assertEqual(Point.distance(p2, p1), 5)

    def test_distance2(self):
        p1 = Point(0, 0)
        p2 = Point(0, 5)

        self.assertEqual(Point.distance(p2, p1), 5)

if __name__ == "__main__":
    unittest.main()