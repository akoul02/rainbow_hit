import math
import random
from collections import deque
from typing import List

from server.game.bots_code.code import continuemain
from server.game.engine.gameobjects.bots.bot import Bot
from server.game.engine.gameobjects.bots.user_bot import UserBot
from server.game.engine.gameobjects.wall import Wall
from server.game.engine.utils.direction import Direction
from server.game.engine.utils.math_utils import get_angle
from server.game.engine.utils.point import Point


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
                # if not (current + dst in steps):
                return True
        return False

    def how_close(obj_fin: Point, obj_start: Point, dirr: Direction):
        item_vector = Point(obj_fin.x - obj_start.x, obj_fin.y - obj_start.y)
        angle = math.acos(get_angle(item_vector, dirr))
        return angle

    def closest(avoid_list: List[Point], directions: List[Direction], obj_start: Point, obj_fin: Point, real: bool,
                coord: Point, objects: List, steps: List):
        close_enough = None
        dif = math.pi if real else 0
        for dirr in directions:
            if check(objects, dirr + coord, coord, steps) and dirr not in avoid_list:
                if real:
                    if how_close(obj_fin, obj_start, dirr) < dif:
                        dif = how_close(obj_fin, obj_start, dirr)
                        close_enough = dirr
                else:
                    if how_close(obj_fin, obj_start, dirr) > dif:
                        dif = how_close(obj_fin, obj_start, dirr)
                        close_enough = dirr
        return close_enough

    directions = Direction.to_list()
    clean_directions = Direction.to_list()
    bot_prew = None
    steps = []

    while True:
        objects = [[False] * 16 for i in range(16)]
        avoid_list = []
        if bot_prew is not None:
            avoid_list.append(bot_prew)

        shooted = False
        for obj in bot.scan():
            if isinstance(obj, UserBot):
                avoid_list.append(
                    closest(avoid_list, clean_directions, bot.current_location(), obj.current_location(), True,
                            bot.coord, objects, steps))
                # steps.append(bot.coord.copy())
                step_directions.append(
                    closest(avoid_list, clean_directions, bot.current_location(), obj.current_location(), False,
                            bot.coord, objects, steps))
                bot_prew = closest(avoid_list, clean_directions, bot.current_location(), obj.current_location(), True,
                                   bot.coord, objects, steps)

        for obj in bot.scan():
            if isinstance(obj, Wall):
                objects[obj.coord.x][obj.coord.y] = True
                print(avoid_list)
                print(closest(avoid_list, clean_directions, bot.current_location(), obj.current_location(), True,
                              bot.coord, objects, steps))
                if closest(avoid_list, clean_directions, bot.current_location(), obj.current_location(), True,
                           bot.coord, objects, steps) is not None:
                    avoid_list.append(
                        closest(avoid_list, clean_directions, bot.current_location(), obj.current_location(), True,
                                bot.coord, objects, steps))
                    print('sdffgnw;erngwrg')
                else:
                    pass
                    # print('aaSD?ASDAS')
                    # bot.shoot(bot.scan()[0])

        random.shuffle(directions)

        for idx in range(len(directions)):
            # print(directions[idx] not in avoid_list and not(check(objects, Point(bot.coord.x + directions[idx].x, bot.coord.y + directions[idx].y), bot.coord, steps)))
            if not (check(objects, Point(bot.coord.x + directions[idx].x, bot.coord.y + directions[idx].y), bot.coord,
                          steps)) and directions[idx] not in avoid_list:
                idx = 0
                step_directions.append(directions[idx])
                # print(step_directions)
                bot.step(directions[idx])
                break
            else:
                continue
            if idx == len(directions) - 1:
                # steps.append(bot.coord.copy())
                try:
                    print(step_directions)
                    direction = step_directions.pop()
                    bot.step(direction)
                except:
                    bot.shoot(bot.scan()[0])
