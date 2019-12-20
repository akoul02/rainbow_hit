from tkinter import Canvas, Tk, Button, messagebox
from tkinter import *
import random
from PIL import Image, ImageTk
from dataclasses import dataclass
from objects.UFO import Ufo
from objects.cloud import Cloud
from constants import *


class Client:
    """Base client class.
    """
    def __init__(self):
        """Initialising values and creating the window with game world
        """
        self.root = Tk()
        self.root.title("RAINBOW hit")
        self.canvas = Canvas(self.root, width=WIDTH * 1.8, height=HEIGHT, bg="white")
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if i == 0 or j == 0 or i == GRID_SIZE - 1 or j == GRID_SIZE - 1:
                    continue
                self.canvas.create_rectangle(i * CELL_SIZE, j * CELL_SIZE,
                                             i * CELL_SIZE + CELL_SIZE,
                                             j * CELL_SIZE + CELL_SIZE, fill='pink', outline='#999090')
        self.canvas.create_rectangle(32, 32, HEIGHT - 32, HEIGHT - 32, outline='black', width=2)
        self.canvas.grid(column=0, row=0)
        pilImage1 = Image.open("./sources/client/assets/ufo1.png")
        self.image1 = ImageTk.PhotoImage(pilImage1)
        self.canvas.create_image(592, 48, image=self.image1)
        self.health1 = self.canvas.create_rectangle(630, 36, 1010, 58, fill='green')
        pilImage2 = Image.open("./sources/client/assets/ufo2.png")
        self.image2 = ImageTk.PhotoImage(pilImage2)
        self.canvas.create_image(592, 90, image=self.image2)
        self.health2 = self.canvas.create_rectangle(630, 78, 1010, 100, fill='green')
        self.text = self.canvas.create_text(632, 138, font="Times", text='Enter Your code:')
        message_entry = Text(width=56, height=22)
        message_entry.place(x=566, y=168)
        self.window = self.canvas.create_rectangle(566, 168, 1018, 524, width=5, outline='#f21d1d')
        message_button = Button(text="Send", width=64)
        message_button.place(x=564, y=540)

    def creating_game_objects(self):
        """Creating Ufos and clouds
        """
        self.ufo_1 = Ufo(48, 48, self.canvas, "./sources/client/assets/ufo1.png")
        self.ufo_2 = Ufo(48 + 32*3, 208, self.canvas, "./sources/client/assets/ufo2.png")
        self.cloud = Cloud(48, 80+32*2, self.canvas, "./sources/client/assets/Cloud.png")
        self.cloud1 = Cloud(48, 80+32*1, self.canvas, "./sources/client/assets/Cloud.png")
        self.cloud2 = Cloud(48+32*2, 80, self.canvas, "./sources/client/assets/Cloud.png")
        self.cloud3 = Cloud(48+32*10, 80, self.canvas, "./sources/client/assets/Cloud.png")
        self.cloud4 = Cloud(48, 80+32*4, self.canvas, "./sources/client/assets/Cloud.png")
        self.cloud5 = Cloud(48+32*9, 80, self.canvas, "./sources/client/assets/Cloud.png")

    def actions(self):
        """Commands processing and visualising actions: move, fire
        """
        self.root.bind('1' + '<Right>', self.ufo_1.move)
        self.root.bind('2' + '<Right>', self.ufo_2.move)
        self.root.bind('<Down>', self.ufo_2.laser)
        self.root.bind('<Up>', self.ufo_2.deleter)
        self.root.mainloop()


client = Client()
client.creating_game_objects()
client.actions()
