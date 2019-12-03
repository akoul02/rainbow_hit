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


    # print(f'Step: 0')
    # playerExecutor.run()
    # main_event.wait()
    # main_event.clear()

    # enemyExecuror.run()
    # main_event.wait()
    # main_event.clear()

    for step in range(1, 8):
        print(f'Step: {step}')
        try:
            playerExecutor.next_move()
            main_event.wait()
            main_event.clear()
        except Bot.ActionsAreOver:
            print('Player actions are over')
            # playerExecutor.thread.join()
            # playerExecutor.bot.sleep()
            # main_event.wait()
            # main_event.clear()

        try:
            enemyExecuror.next_move()
            main_event.wait()
            main_event.clear()
        except Bot.ActionsAreOver:
            print('Enemy actions are over')
            # enemyExecuror.thread.join()
            # enemyExecuror.bot.sleep()
            # main_event.wait()
            # main_event.clear()




if __name__ == "__main__":
    main()