from tkinter import *
import random
from PIL import Image, ImageTk

# Создаем окно
root = Tk()
# Устанавливаем название окна
root.title("RAINBOW hit")
GRID_SIZE = 15
SQUARE_SIZE = 32
# ширина экрана
WIDTH = GRID_SIZE * SQUARE_SIZE
# высота экрана
HEIGHT = GRID_SIZE *SQUARE_SIZE
# Размер сегмента танка
SEG_SIZE = 30
# Переменная отвечающая за состояние игры(взять у ребят с серверной части)
IN_GAME = True


c = Canvas(root, width=WIDTH, height=HEIGHT)


for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        c.create_rectangle(i * SQUARE_SIZE, j * SQUARE_SIZE,
                           i * SQUARE_SIZE + SQUARE_SIZE,
                           j * SQUARE_SIZE + SQUARE_SIZE, fill='#'+str(random.randint(600000, 999999)))
c.grid(column=0, row=0)

c.pack()
pilImage = Image.open("redu.png")
image = ImageTk.PhotoImage(pilImage)
imagesprite = c.create_image(100, 100, image=image)
c.mainloop()