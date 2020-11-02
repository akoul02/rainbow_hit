from PIL import Image, ImageTk
from ..const_client import *
from dataclasses import dataclass
from tkinter import Canvas, Tk


class Ufo:
    """Class of UFO. Create it and process actions

    Attributes
    ----------
    x : int
    y : int

    canvas : Canvas
        game filled

    sprite : Canvas
        photos of UFOs on canvas

    name : str
        unique identifier of UFOs

    health : int
    max_health: int
    damage : int
    """

    def __init__(self, x, y, canvas, way, name, health, damage):
        """Initialising values and creation UFO
        """
        self.x = x
        self.y = y
        self.canvas = canvas
        self.image = ImageTk.PhotoImage(Image.open(way))
        self.sprite = self.canvas.create_image(self.x, self.y, image=self.image)

        self.explosion_img = ImageTk.PhotoImage(Image.open(way.parent / "explosion.png"))

        self.name = name
        self.health = health
        self.max_health = health
        self.damage = damage

    def move(self, x, y, Event=None):
        """Moving UFO to adjacent cell

        Parameters
        ----------
        x : int
        y : int

        Returns
        -------
        None
        """
        self.canvas.move(self.sprite, (48 + x * 32) - self.x, (32 * 18 - (48 + y * 32)) - self.y)
        self.x, self.y = self.canvas.coords(self.sprite)

    def laser(self, x, y, Event=None):
        """Laser from UFO to given coordinates

        Parameters
        ----------
        x : int
        y : int

        Returns
        -------
        None
        """
        x1, y1 = self.canvas.coords(self.sprite)
        canvas_id = self.canvas.create_line(x1, y1, 48 + x * 32, 32 * 18 - (48 + y * 32), fill='red', width='3')
        self.canvas.after(LASER_TIMEOUT, self.canvas.delete, canvas_id)

        explosion_id = self.canvas.create_image(48 + x * 32, 32 * 18 - (48 + y * 32), image=self.explosion_img)
        self.canvas.after(EXPLOSION_TIMEOUT, self.canvas.delete, explosion_id)

    def deleter(self, Event=None):
        """Delete UFO if it dies

        Returns
        -------
        None
        """
        self.canvas.delete(self.sprite)
