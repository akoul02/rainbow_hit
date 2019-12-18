from tkinter import Canvas
from PIL import Image, ImageTk

from constants import *


class Cloud:
    def __init__(self, x, y, canvas, way):
        self.x = x
        self.y = y
        self.pilImage = Image.open(way)
        self.image = ImageTk.PhotoImage(self.pilImage)
        self.canvas = canvas
        self.sprite = self.canvas.create_image(self.x, self.y, image=self.image)
