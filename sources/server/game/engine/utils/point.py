from __future__ import annotations

from dataclasses import dataclass
from math import sqrt, pow

@dataclass
class Point:
    '''Class, that represent one point
    '''
    x: int
    y: int

    def __eq__(self, pt):
        return self.x == pt.x and self.y == pt.y

    def distance_to(self, b: Point):
        return sqrt(pow(self.x - b.x, 2) + pow(self.y - b.y, 2)) 

    @staticmethod
    def distance(a: Point, b: Point):
        return sqrt(pow(a.x - b.x, 2) + pow(b.y - b.y, 2))