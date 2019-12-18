from dataclasses import dataclass
from tkinter import Canvas, Tk
from PIL import Image, ImageTk
from constants import *


class Ufo:
    def __init__(self, x, y, canvas, way):
        self.x = x
        self.y = y
        self.pilImage = Image.open(way)
        self.image = ImageTk.PhotoImage(self.pilImage)
        self.canvas = canvas
        self.sprite = self.canvas.create_image(self.x, self.y, image=self.image)

    def move(self, cmd, Event=None):
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
        x1, y1 = self.canvas.coords(self.sprite)
        canvas_id = self.canvas.create_line(x1, y1, x, y, fill='red', width='3')
        self.canvas.after(LASER_TIMEOUT, self.canvas.delete, canvas_id)

    def deleter(self, Event=None):
        self.canvas.delete(self.sprite)
