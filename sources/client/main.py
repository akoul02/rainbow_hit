from tkinter import Canvas, Tk, Button, messagebox
import random
from PIL import Image, ImageTk
from dataclasses import dataclass
from objects.UFO import Ufo
from objects.cloud import Cloud
from const_client import *
import json

class Client:
    """Base client class.
    """
    def __init__(self, trace_path):
        """Initialising values and creating the window with game world
        """
        self.trace_path = trace_path
        self.game_data = json.loads(open(trace_path, 'r').read())

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
        self.game_over = False
        self.step = 0
        self.steps_text = self.canvas.create_text(632, 138, font="Times", text='Current step: 0')

        self.updater_job = None
        # message_entry = Text(width=56, height=22)
        # message_entry.place(x=566, y=168)
        # self.window = self.canvas.create_rectangle(566, 168, 1018, 524, width=5, outline='#f21d1d')
        self.start_button = Button(text="start", width=32, command=self.updater)
        self.start_button.place(x=564, y=200)

        self.step_button = Button(text="step", width=32, command=self.step_once)
        self.step_button.place(x=564, y=240)

        self.pause_btn = Button(text="pause", width=32, command=self.pause)
        self.pause_btn.place(x=564, y=280)

    def get_object(self, x, y):
        for obj in self.objects:
            objx, objy = self.canvas.coords(obj.sprite)
            if objx == 48 + x * 32.0 and objy == 32.0 * 18 - (48 + y * 32):
                return obj
        return None

    def pop_object(self, x, y):
        for idx in range(len(self.objects)):
            objx, objy = self.canvas.coords(self.objects[idx].sprite)
            if objx == 48 + x * 32.0 and objy == 32.0 * 18 - (48 + y * 32):
                return self.objects.pop(idx)
        return None

    def get_ufo_by_name(self, name):
        for obj in self.objects:
            if isinstance(obj, Ufo):
                if obj.name == name:
                    return obj
        return None
    
    def creating_game_objects(self):
        """Creating Ufos and clouds
        """
        self.objects = []
        for k, v in self.game_data[0]['init_world'].items():
            x, y = eval(k) 
            if v[0] == 'Bot' and v[1] == 'player1':
                self.objects.append(Ufo(48 + x * 32, 32 * 18 - (48 + y * 32), self.canvas, "./sources/client/assets/ufo1.png", 'player1'))
            elif v[0] == 'Bot' and v[1] == 'player2':
                self.objects.append(Ufo(48 + x * 32, 32 * 18 - (48 + y * 32), self.canvas, "./sources/client/assets/ufo2.png", 'player2'))
            else:
                self.objects.append(Cloud(48 + x * 32, 32 * 18 - (48 + y * 32), self.canvas, "./sources/client/assets/Cloud.png"))            
        
        self.game_data.pop(0)

    def actions(self):
        """Commands processing and visualising actions: move, fire
        """
        self.root.bind('1' + '<Right>', self.ufo_1.move)
        self.root.bind('2' + '<Right>', self.ufo_2.move)
        self.root.bind('<Down>', self.ufo_2.laser)
        self.root.bind('<Up>', self.ufo_2.deleter)

    def pause(self, event=None):
        if self.updater_job != None:
            self.root.after_cancel(self.updater_job)

    def updater(self, event=None):
        self.step_once()
        self.updater_job = self.root.after(100, self.updater)

    def step_once(self, event=None):
        if self.game_over:
            return None
        
        cmd = self.game_data.pop(0)
        if list(cmd.keys())[0] == 'sleep':
            pass
        elif list(cmd.keys())[0] == 'step':
            player = cmd['step']['player']
            newx = cmd['step']['new_x']
            newy = cmd['step']['new_y']

            player_ufo = self.get_ufo_by_name(player)
            player_ufo.move(newx, newy)

        elif list(cmd.keys())[0] == 'shoot':
            player = cmd['shoot']['player']
            x_end = cmd['shoot']['x_end']
            y_end = cmd['shoot']['y_end']
            destroyed = cmd['shoot']['destroyed']

            player_ufo = self.get_ufo_by_name(player)
            player_ufo.laser(x_end, y_end)
            if destroyed:
                obj = self.pop_object(x_end, y_end)
                self.root.after(70, func=obj.deleter)

        elif list(cmd.keys())[0] == 'game_over':
            self.game_over = True
            if cmd['game_over']['draw'] == True:
                messagebox.showinfo("GAME OVER", "Draw!")
            else:
                messagebox.showinfo("GAME OVER", f"Winner is: {cmd['game_over']['winner']}")

        if not self.game_over:
            self.step += 1
            self.canvas.itemconfigure(self.steps_text, text=f'Current step: {self.step}')

    def main_loop(self):
        self.root.mainloop()
