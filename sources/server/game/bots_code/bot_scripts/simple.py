import random
import time
import math
from collections import deque
from server.game.bots_code.code import continuemain
from server.game.engine.gameobjects.bots.bot import Bot
from server.game.engine.gameobjects.bots.user_bot import UserBot
from server.game.engine.gameobjects.destroyable import Destroyable
from server.game.engine.gameobjects.wall import Wall
from server.game.engine.utils.direction import Direction
from server.game.engine.utils.point import Point
from server.game.exceptions import *
from server.game.engine.utils.math_utils import get_angle
from typing import Any, List


@continuemain
def perform(bot: Bot):
    objects = [[False] * 16 for i in range(16)]
    # queue for steps (last 6)
    steps: deque = deque([], 10)
    step_directions: deque = deque([], 10)

    def at_position(world: List[List[bool]], coord: Point) -> bool:
        if world[coord.x][coord.y]:
            return True
        return False

    def check(world: List[List[bool]], dst: Point, current: Point, steps: deque) -> bool:
        if current.x + dst.x >= 0 and current.x + dst.x < 16 and current.y + dst.y >= 0 and current.y + dst.y < 16:
            if not at_position(world, current + dst):
                if not (current + dst in steps):
                    return True
        return False

    def get_closest_dir(obj_fin: Point, obj_start: Point):
        directions = list(Direction)
        item_vector = Point(obj_fin.x - obj_start.x, obj_fin.y - obj_start.y)
        dif = math.pi
        best = None

        for dirr in directions:
            if math.acos(get_angle(item_vector, dirr._value_)) < dif:
                best = dirr
                dif = math.acos(get_angle(item_vector, dirr._value_))
        return best

    def closest(avoid_list: List[Direction], directions: List[Direction], best_direction: Direction):
        close_enough = directions[0]
        for dirr in directions:
            if dirr not in avoid_list:
                if best_direction.distance_to(dirr):
                    close_enough = dirr
        return close_enough

    directions = list(Direction)
    clean_directions = list(Direction)

    while True:
        avoid_list = []

        for obj in bot.scan():
            if isinstance(obj, Wall):
                objects[obj.coord.x][obj.coord.y] = True
                avoid_list.append(get_closest_dir(bot.current_location(), obj.current_location()))

        shooted = False
        for obj in bot.scan():
            if isinstance(obj, UserBot):
                avoid_list.append(get_closest_dir(bot.current_location(), obj.current_location()))
                print("asdsadsa")
                print(closest((avoid_list, directions,
                               ~get_closest_dir(bot.current_location(), obj.current_location()))))
                bot.step(closest((avoid_list, directions,
                                  ~get_closest_dir(bot.current_location(), obj.current_location()))))

        random.shuffle(directions)
        if not shooted:
            for idx in range(len(directions)):
                if check(objects, directions[idx].value, bot.coord, steps):
                    steps.append(bot.coord.copy())
                    step_directions.append(directions[idx])
                    bot.step(directions[idx])
                    idx = 0
                    break
                else:
                    continue
