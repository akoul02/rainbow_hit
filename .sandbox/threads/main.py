from threading import Barrier, Thread, Lock, Event
from executor import Executor
from playerCode import *
from time import sleep
from bot import Bot

def main():
    # used to lock main Thread
    main_event = Event()
    playerExecutor = Executor(Bot(0, 'player', main_event), run_user)
    enemyExecuror  = Executor(Bot(0, 'enemy', main_event),  run_enemy)

    playerExecutor.run()
    main_event.wait()
    main_event.clear()

    playerExecutor.next_move()
    main_event.wait()
    main_event.clear()

    playerExecutor.next_move()
    main_event.wait()
    main_event.clear()

    # for step in range(0, 8):
    #     print(f'Step: {step}')
    #     sync.next_move()


if __name__ == "__main__":
    main()