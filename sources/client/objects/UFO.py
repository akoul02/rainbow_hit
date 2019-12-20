from dataclasses import dataclass
from tkinter import Canvas, Tk
from PIL import Image, ImageTk
from const_client import *


class Ufo:
    """Class of UFO. Create it and process actions
    """
    def __init__(self, x, y, canvas, way, name):
        """Initialising values and creation UFO
        """
        self.x = x
        self.y = y
        self.pilImage = Image.open(way)
        self.image = ImageTk.PhotoImage(self.pilImage)
        self.canvas = canvas
        self.sprite = self.canvas.create_image(self.x, self.y, image=self.image)
        self.name = name

    def move(self, x, y, Event=None):
        """Moving UFO to adjacent cell
        """
        self.canvas.move(self.sprite, (48 + x * 32) - self.x, (32 * 18 - (48 + y * 32)) - self.y)
        self.x, self.y = self.canvas.coords(self.sprite)

    def laser(self, x, y, Event=None):
        """Laser from UFO to given coordinates
        """
        x1, y1 = self.canvas.coords(self.sprite)
        canvas_id = self.canvas.create_line(x1, y1, 48 + x * 32, 32 * 18 - (48 + y * 32), fill='red', width='3')
        self.canvas.after(LASER_TIMEOUT, self.canvas.delete, canvas_id)

    def deleter(self, Event=None):
        """Delete UFO if it dies
        """
        self.canvas.delete(self.sprite)
