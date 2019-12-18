import unittest
from tkinter import Canvas, Tk

import sys, os
sys.path.insert(0, os.path.dirname(__file__)+'/../')

from objects.UFO import Ufo
from constants import *

class Move_tests(unittest.TestCase):
    def test_1(self):
        root = Tk()
        canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg="white")

        test_object = Ufo(48, 48, canvas, "C:/Users/varya/Desktop/rainbow_hit/sources/client/assets/ufo1.png")
        test_object.creation()
        x1, y1 = test_object.canvas.coords(test_object.sprite)
        test_object.move()
        x2, y2 = test_object.canvas.coords(test_object.sprite)
        self.assertEqual(x2-x1, 32, 'x_position_mistake')
        self.assertEqual(y2-y1, 0, 'y_position_mistake')



if __name__ == '__main__':
    unittest.main()
