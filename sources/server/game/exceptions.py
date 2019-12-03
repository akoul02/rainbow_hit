class GameException(Exception):
    pass

class InvalidSelfInstance(GameException):
    def __init__(self, msg):
        GameException.__init__(self, 'Invalid type of self object!')