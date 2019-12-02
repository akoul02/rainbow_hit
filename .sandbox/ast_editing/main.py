from bot import Bot
import playerCode
import yieldifier

def main():
    p1 = Bot(0, 'player')
    e1 = Bot(0, 'enemy')
    runUser_mod = yieldifier.ast_yieldify(playerCode.__file__, 'runUser')
    runEnemy_mod = yieldifier.ast_yieldify(playerCode.__file__, 'runEnemy')

    objects = [(p1, runUser_mod(p1)), (e1, runEnemy_mod(e1))]

    for step in range(1, 8):
        print(step)
        for obj in objects:
            try:
                next(obj[1])
            except StopIteration:
                obj[0].sleep()
                
if __name__ == "__main__":
    main()