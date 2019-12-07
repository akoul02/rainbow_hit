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

class BotTimeoutError(GameException, TimeoutError):
    '''Exception, which get raised, 
    if the bot thread runs longer than it should
    '''
    def __init__(self):
        GameException.__init__(self, 'Bot thread time is over!')

class ThreadKilledError(GameException):
    '''Exception, which get raised, 
    if the user-thread was killed, and player still trying to use it
    '''
    def __init__(self):
        GameException.__init__(self, 'User thread killed!')

class FatalException(Exception):
    '''FatalError

    after this exception execution cannot be continued
    '''
    def __init__(self, msg):
        Exception.__init__(msg)