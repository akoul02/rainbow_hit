from tkinter import Canvas, Tk
import random
from PIL import Image, ImageTk
from dataclasses import dataclass
from objects.tank import Tank
from constants import *

class Client:
    def __init__(self):
        self.root = Tk()
        self.root.title("RAINBOW hit")
        self.canvas = Canvas(self.root, width=WIDTH, height=HEIGHT, bg="white")

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if i == 0 or j == 0 or i == GRID_SIZE - 1 or j == GRID_SIZE - 1:
                    continue
                self.canvas.create_rectangle(i * CELL_SIZE, j * CELL_SIZE,
                                   i * CELL_SIZE + CELL_SIZE,
                                   j * CELL_SIZE + CELL_SIZE, fill='pink', outline='#999090')
        self.canvas.create_rectangle(32, 32, HEIGHT - 32, HEIGHT - 32, outline='black', width=2)
        self.canvas.grid(column=0, row=0)
        self.canvas.pack()

    def start(self):
        tank_red = Tank(48, 48, self.canvas, "C:/Users/varya/Desktop/rainbow_hit/sources/client/assets/redd.png")
        tank_red.creation()
        tank_green = Tank(208, 208, self.canvas, "C:/Users/varya/Desktop/rainbow_hit/sources/client/assets/greend.png")
        tank_green.creation()
        self.root.bind('1'+'<Right>', tank_red.move)
        self.root.bind('<Left>', tank_green.move)
        self.root.bind('<Up>', tank_red.rotation)
        self.root.bind('<Down>', tank_green.laser)
        self.root.mainloop()

client = Client()
client.start()

