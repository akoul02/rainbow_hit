class GameException(Exception):
    pass

class InvalidSelfInstance(GameException):
    def __init__(self):
        GameException.__init__(self, 'Invalid type of self object!')

class StepsAreOver(GameException):
    '''Exception, which get raised, if steps are over
    '''
    def __init__(self):
        GameException.__init__(self, 'Steps are over!')

class ActionsAreOver(GameException):
    '''Exception, which get raised, if bot actions are over
    '''
    def __init__(self):
        GameException.__init__(self, 'Bot actions are over!')