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

    def move(self, cmd, Event=None):
        """Moving UFO to adjacent cell
        """
        if 'Up' in cmd:
            self.canvas.move(self.sprite, 0, -CELL_SIZE)
        if 'Down' in cmd:
            self.canvas.move(self.sprite, 0, CELL_SIZE)
        if 'Left' in cmd:
            self.canvas.move(self.sprite, -CELL_SIZE, 0)
        if 'Right' in cmd:
            self.canvas.move(self.sprite, CELL_SIZE, 0)
        self.x, self.y = self.canvas.coords(self.sprite)

    def laser(self, x, y, Event=None):
        """Laser from UFO to given coordinates
        """
        x1, y1 = self.canvas.coords(self.sprite)
        canvas_id = self.canvas.create_line(x1, y1, x, y, fill='red', width='3')
        self.canvas.after(LASER_TIMEOUT, self.canvas.delete, canvas_id)

    def deleter(self, Event=None):
        """Delete UFO if it dies
        """
        self.canvas.delete(self.sprite)
