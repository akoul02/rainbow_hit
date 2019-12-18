from tkinter import Canvas
from PIL import Image, ImageTk
from constants import *


class Cloud:
    """Creating and deleting clouds
    """
    def __init__(self, x, y, canvas, way):
        """Create cloud on x, y coordinates
        """
        self.x = x
        self.y = y
        self.pilImage = Image.open(way)
        self.image = ImageTk.PhotoImage(self.pilImage)
        self.canvas = canvas
        self.sprite = self.canvas.create_image(self.x, self.y, image=self.image)
    def deleter(self, Event=None):
        """Delete Cloud if it dies
        """
        self.canvas.delete(self.sprite)