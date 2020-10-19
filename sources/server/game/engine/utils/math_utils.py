import math

from server.game.engine.utils.point import Point

'''Simple math functions
'''


def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)


def samelcheck(ox, oy, x1, x2, y1, y2):
    if y1 == y2:
        if y1 == y2 == oy:
            return True
        else:
            return False
    elif x1 == x2:
        if x1 == x2 == ox:
            return True
        else:
            return False
    elif (ox - x1) / (x2 - x1) == (oy - y1) / (y2 - y1):
        return True


def get_angle(obj_first: Point, obj_second: Point):
    try:
        a = ((obj_first.x * obj_second.x + obj_first.y * obj_second.y) / (
                math.sqrt(math.pow(obj_first.x, 2) + math.pow(obj_second.x, 2)) * math.sqrt(
            math.pow(obj_first.y, 2) + math.pow(obj_second.y, 2))))
    except:
        a = -1
        # print(obj_first.x, obj_first.y, obj_second.x, obj_second.y)
    return a
