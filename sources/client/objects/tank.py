from dataclasses import dataclass
from tkinter import Canvas, Tk
from objects.gameobject import GameObject
from PIL import Image, ImageTk
from constants import *


class Tank(GameObject):
    def __init__(self, x, y, canvas, way):
        self.x = x
        self.y = y
        self.pilImage = Image.open(way)
        self.image = ImageTk.PhotoImage(self.pilImage)
        self.canvas = canvas

    def move(self, Event=None):
        self.canvas.move(self.sprite, 32, 0)
        self.x, self.y = self.canvas.coords(self.sprite)

    def laser(self, Event=None):
        x, y = self.canvas.coords(self.sprite)
        canvas_id = self.canvas.create_line(x, y, 32, 300, fill='red', width='3')
        self.canvas.after(LASER_TIMEOUT, self.canvas.delete, canvas_id)

    def rotation(self, Event=None):
        self.canvas.delete(self.sprite)
        self.pilImage = self.pilImage.rotate(45)
        self.image = ImageTk.PhotoImage(self.pilImage)
        self.sprite = self.canvas.create_image(self.x, self.y, image=self.image)

    def creation(self):
        self.sprite = self.canvas.create_image(self.x, self.y, image=self.image)
