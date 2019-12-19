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
    elif (ox - x1)/(x2 - x1) == (oy - y1)/(y2 - y1):
        return True