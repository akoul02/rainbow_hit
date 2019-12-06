class GameException(Exception):
    '''Base class for all in-game exceptions.
    '''
    pass

class InvalidSelfInstance(GameException):
    '''Raised, when invalid object passed in args[0]
    '''
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