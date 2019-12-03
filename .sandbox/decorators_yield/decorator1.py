def delay(fun):
    def do(*args, **kwargs):
        def really_do(actions):
            return fun(actions, *args, **kwargs)
        return really_do
    return do

class Actions:
    pos : float = 0
    @delay
    def move(self, distance):
        self.pos += distance

def user():
    while True:
        yield Actions.move(1)

actions1 = Actions()
actions2 = Actions()
user1 = user()
user2 = user()

while actions1.pos < 10:
    command = next(user1)
    command(actions1)

    command = next(user2)
    command(actions2)

print(actions1.pos)
print(actions2.pos)
