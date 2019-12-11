from dataclasses import dataclass
from objects.gameobject import GameObject
from constants import *

@dataclass
class Tank(GameObject):
    pass
    # def move(self, Event=None):
    #     self.canvas.move(self.sprite, CELL_SIZE, 0)
    #
    # def laser(self, x, y, Event=None):
    #     canvas_id = self.canvas.create_line(self.x, self.y, x, y, fill='red', width='3')
    #     self.canvas.after(LASER_TIMEOUT, self.canvas.delete, canvas_id)