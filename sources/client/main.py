from tkinter import *

# Создаем окно
root = Tk()
# Устанавливаем название окна
root.title("RAINBOW hit")

GRID_SIZE = 10
SQUARE_SIZE = 50
# ширина экрана
WIDTH = GRID_SIZE * SQUARE_SIZE
# высота экрана
HEIGHT = GRID_SIZE *SQUARE_SIZE
# Размер сегмента танка
SEG_SIZE = 30
# Переменная отвечающая за состояние игры(взять у ребят с серверной части)
IN_GAME = True

# заливаем все зеленым цветом
c = Canvas(root, width=WIDTH, height=HEIGHT, bg="#105410")
#делаем сетку
for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        c.create_rectangle(i * SQUARE_SIZE, j * SQUARE_SIZE,
                           i * SQUARE_SIZE + SQUARE_SIZE,
                           j * SQUARE_SIZE + SQUARE_SIZE)
c.grid(column=0, row=0)
c.mainloop()
