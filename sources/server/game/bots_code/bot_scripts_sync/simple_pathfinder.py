from random import randint
from typing import Union

from server.game.bots_code.code_dummy import BotActivityDummy
from server.game.engine.gameobjects.bots.bot_sync import Bot
from server.game.engine.gameobjects.destroyable import Destroyable
from server.game.engine.gameobjects.wall import Wall
from server.game.engine.utils.direction import Direction
from server.game.engine.utils.point import Point


class BotActivity:
    def __init__(self, bot: BotActivityDummy):
        self.bot = bot

        self.objects = None
        self.target_visited = []

        self.last_step = None
        self.shoot_enemy_last_step = False

        self.temporary_path_visited = []
        self.current_target = None
        self.current_avoid_direction = None

        self.enemy_in_range = False
        self.shoot_them = False
        self.last_enemy_pos = Point(-1, -1)

    def perform(self):
        self.update()
        if self.shoot_enemy_last_step:
            self.shoot_enemy_last_step = False
            self.bot.step(~Direction(self.last_step))
            self.clear_logic()  # optional move
            return
        if self.enemy_in_range:
            self.bot.shoot(self.last_enemy_pos)
            self.shoot_enemy_last_step = True
            return
        if self.shoot_them:
            self.bot.shoot(self.current_target)
            self.shoot_them = False
            return

        self.check_target()
        best_dir = self.best_direction()
        if best_dir:
            self.last_step = best_dir
            self.bot.step(best_dir)

    def check_target(self):
        if self.current_target is None:
            self.current_target = self.get_random_point()

    def update(self):
        self.objects = [[-1] * 16 for i in range(16)]
        self.enemy_in_range = False
        for obj in self.bot.scan():
            if isinstance(obj, Wall) and obj.is_alive():
                self.objects[obj.coord.x][obj.coord.y] = 1
                if self.current_target is not None and obj.coord == self.current_target:
                    self.shoot_them = True
            elif isinstance(obj, Bot) and obj.is_alive():
                self.objects[obj.coord.x][obj.coord.y] = 2
                self.enemy_in_range = True
                self.last_enemy_pos = obj.coord

    def best_direction(self) -> Union[Direction, Point, bool]:
        current_pos = self.bot.current_location()
        vec = self.current_target - current_pos
        dr = Point(0, 0)
        dr.x = vec.x // abs(vec.x) if vec.x != 0 else 0
        dr.y = vec.y // abs(vec.y) if vec.y != 0 else 0

        if dr == Point(0, 0):  # пришли
            self.target_visited.append(self.current_target)
            self.clear_logic()
            self.check_target()
            return self.best_direction()

        new_pos = current_pos + dr
        if self.objects[new_pos.x][new_pos.y] > 0:
            d_list = Direction.to_list()
            i = d_list.index(dr)
            k = i
            while self.objects[new_pos.x][new_pos.y] > 0 or new_pos in self.temporary_path_visited:
                if self.current_avoid_direction == 1:
                    k += 1
                    if k > 7:
                        k = 0
                    if not self.check(current_pos + d_list[k]):
                        continue
                    new_pos = current_pos + d_list[k]
                else:
                    k -= 1
                    if k < 0:
                        k = 7
                    if not self.check(current_pos + d_list[k]):
                        continue
                    new_pos = current_pos + d_list[k]

                if k == i:
                    t = current_pos + dr
                    if self.objects[t.x][t.y] < 0:
                        return dr
                    self.bot.shoot(current_pos + dr)
                    return False
            self.temporary_path_visited.append(new_pos)
            return d_list[k]
        else:
            self.temporary_path_visited.append(new_pos)
            return dr

    def check(self, dst: Point) -> bool:
        if 0 <= dst.x < 16 and 0 <= dst.y < 16:
            return True
        return False

    def clear_logic(self):
        self.current_target = None
        self.temporary_path_visited = []
        self.current_avoid_direction = None

    def get_random_point(self) -> Point:
        p = Point(randint(0, 15), randint(0, 15))
        while p in self.target_visited:
            p = Point(randint(0, 15), randint(0, 15))

        self.current_avoid_direction = randint(1, 2)
        return p
