class Delayed:
    '''Stores the function name and arguments to be called later'''
    def __init__(self, name, args, kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs
    def __call__(self, other_self):
        return getattr(other_self, self.name).original(other_self, *self.args, **self.kwargs)
    def __repr__(self):
        return f'Delayed({repr(self.name)}, {repr(self.args)}, {repr(self.kwargs)})'

def delay(fun):
    '''A decorator that delays the method execution until later.

    The call produces an object that can be called later in the event loop.
    All arguments are forwarded to the decorated function.
    One additional argument is specified to act as `self`'''
    name = fun.__name__
    def do(*args, **kwargs):
        return Delayed(name, args, kwargs)
    do.original = fun
    return do

class Actions:
    '''The main class whose methods are called by user program to send commands'''
    pos: float = 0
    @delay
    def move(self, distance: float):
        '''moves the avatar by distance'''
        self.pos += distance

def user():
    '''Moving the avatar forward and only forward'''
    while True:
        yield Actions.move(1)
        
if __name__ == '__main__':
    actions = Actions()
    user1 = user()
    while actions.pos < 10:
        command = next(user1)
        print(command)
        command(actions)
    print(actions.pos)
