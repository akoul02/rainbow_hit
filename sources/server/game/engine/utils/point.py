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

    def distance_to(self, b: Point) -> float:
        '''Find distance between current point and given point b

        Parameters
        ----------
        b : Point
            second point
        
        Returns
        -------
        n : float
            distance between 2 points
        '''
        return sqrt(pow(self.x - b.x, 2) + pow(self.y - b.y, 2)) 

    @staticmethod
    def distance(a: Point, b: Point) -> float:
        '''Static method to find distance between 2 points (a and b)

        Parameters
        ----------
        b : Point
            first point
        
        b : Point
            second point
        
        Returns
        -------
        n : float
            distance between 2 points
        '''
        return sqrt(pow(a.x - b.x, 2) + pow(a.y - b.y, 2))
