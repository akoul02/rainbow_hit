import unittest
from tkinter import Canvas, Tk

import sys, os
sys.path.insert(0, os.path.dirname(__file__) + '/../')

from objects.UFO import Ufo
from const_client import *

class Move_tests(unittest.TestCase):
    def test_1(self):
        root = Tk()
        canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg="white")

        test_object = Ufo(48, 48, canvas, "./sources/client/assets/ufo1.png", 'tmpname', 10, 1)
        x1, y1 = test_object.canvas.coords(test_object.sprite)
        test_object.move(1, 1)
        x2, y2 = test_object.canvas.coords(test_object.sprite)
        self.assertEqual(x2-x1, 32, 'x_position_mistake')
        self.assertEqual(y2-y1, 448, 'y_position_mistake')

if __name__ == '__main__':
    unittest.main()
