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

    # def movement(self, *args, **kwargs):
    #     self.сanvas.move(self.imagesprite, 0, -32)
    #
    # def lazer(self, *args, **kwargs):
    #     canvas_id = self.сanvas.create_line(48, 48, 48, self.WIDTH - 32, fill='red', width='3')
    #     self.сanvas.after(200, self.сanvas.delete, canvas_id)
    #
    # def rotatioon(self):
    #     rotated = Image.open("./assets/greenr.png").rotate(55)
    #     image = ImageTk.PhotoImage(rotated)
    #     img = self.сanvas.create_image(272, 240, image=image)
    #     self.imagegreen
    #     self.сanvas.after(100)

    # def a(self):
    #     pilImage = Image.open("./assets/redd.png")
    #     image = ImageTk.PhotoImage(pilImage)
    #     self.imagesprite = self.сanvas.create_image(48, 80, image=image)
    #
    #     pilImage1 = Image.open("./assets/blueu.png")
    #     imRotate = pilImage1.rotate(45)
    #     image1 = ImageTk.PhotoImage(imRotate)
    #     self.imagesblue = self.сanvas.create_image(self.WIDTH - 80, self.WIDTH - 112, image=image1)
    #
    #     pilImage2 = Image.open("./assets/greenr.png")
    #     image2 = ImageTk.PhotoImage(pilImage2)
    #     self.imagegreen = self.сanvas.create_image(272, 240, image=image2)

    def start(self):
        # pilImage = Image.open("C:/Users/varya/Desktop/rainbow_hit/sources/client/assets/redd.png")
        # image = ImageTk.PhotoImage(pilImage)
        # self.canvas.create_image(48, 48, image=image)

        tank = Tank(48, 48, self.canvas, "C:/Users/varya/Desktop/rainbow_hit/sources/client/assets/redd.png")
        self.root.mainloop()

client = Client()
client.start()