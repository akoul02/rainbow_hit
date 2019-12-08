from tkinter import *
import random
from PIL import Image, ImageTk
from dataclasses import dataclass
# Создаем окно
root = Tk()
# Устанавливаем название окна
root.title("RAINBOW hit")
GRID_SIZE = 16
SQUARE_SIZE = 32
# ширина экрана
WIDTH = GRID_SIZE * SQUARE_SIZE
# высота экрана
HEIGHT = GRID_SIZE *SQUARE_SIZE
# Переменная отвечающая за состояние игры(взять у ребят с серверной части)
IN_GAME = True


c = Canvas(root, width=WIDTH, height=HEIGHT, bg="white")


for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        if i == 0 or j == 0 or i == GRID_SIZE-1 or j == GRID_SIZE-1:
            continue
        c.create_rectangle(i * SQUARE_SIZE, j * SQUARE_SIZE,
                           i * SQUARE_SIZE + SQUARE_SIZE,
                           j * SQUARE_SIZE + SQUARE_SIZE, fill='pink', outline='#999090')
c.create_rectangle(32,32, HEIGHT-32, HEIGHT-32, outline='black', width=2)
c.grid(column=0, row=0)

c.pack()
pilImage = Image.open("redd.png")
image = ImageTk.PhotoImage(pilImage)
imagesprite = c.create_image(48, 80, image=image)


c.pack()
pilImage1 = Image.open("blueu.png")
image1 = ImageTk.PhotoImage(pilImage1)
imagesblue = c.create_image(WIDTH-80, WIDTH-112, image=image1)
c.pack()

pilImage2 = Image.open("greenr.png")
image2 = ImageTk.PhotoImage(pilImage2)
imagegreen = c.create_image(272, 240, image=image2)


def movement(Event=None):
    c.move(imagesprite, 0, -32)
    c.after(10)
def lazer(Event=None):
    c.create_line(48,88,48,480, fill='brown', width=3)
    c.pack()
    c.after(10)
root.bind('<Up>', movement) #or whatever you're binding it to
root.bind('<Down>', lazer)
root.mainloop()
