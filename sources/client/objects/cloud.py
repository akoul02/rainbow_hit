from tkinter import Canvas
from PIL import Image, ImageTk
from const_client import *


class Cloud:
    """Creating and deleting clouds

    Attributes
    ----------
    x : int
    y : int
    canvas : Canvas
        game filled

    sprite : Canvas
        photos of clouds on canvas
    """

    def __init__(self, x, y, canvas, way):
        """Create cloud on x, y coordinates
        """
        self.x = x
        self.y = y
        self.canvas = canvas
        self.image = ImageTk.PhotoImage(Image.open(way))
        self.sprite = self.canvas.create_image(self.x, self.y, image=self.image)

    def deleter(self, Event=None):
        """Delete Cloud if it dies
        """
        self.canvas.delete(self.sprite)