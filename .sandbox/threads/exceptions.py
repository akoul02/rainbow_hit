class GameException(Exception):
    pass

class InvalidSelfInstance(GameException):
    def __init__(self):
        GameException.__init__(self, 'Invalid type of self object!')