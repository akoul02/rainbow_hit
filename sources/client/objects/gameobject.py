from dataclasses import dataclass
from tkinter import Canvas
from PIL import Image, ImageTk

from constants import *

@dataclass
class GameObject:
    x: float
    y: float
    canvas: Canvas
    sprite_path: str
    sprite: Canvas = None

    def __post_init__(self):
        pilImage = Image.open(self.sprite_path)
        image = ImageTk.PhotoImage(pilImage)
        self.sprite = self.canvas.create_image(self.x, self.y, image=image)
