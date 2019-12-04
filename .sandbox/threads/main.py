from threading import Barrier, Thread, Lock, Event
from executor import Executor
from playerCode import *
from time import sleep
import hanging_threads
from bot import Bot

def main():
    # used to lock main Thread

    # hanging_threads.start_monitoring()

    main_event = Event()
    playerExecutor = Executor(Bot(0, 'player', main_event), run_user)
    enemyExecuror  = Executor(Bot(0, 'enemy', main_event),  run_enemy)

    for step in range(1, 8):
        print(f'\nStep: {step}')
        try:
            playerExecutor.next_move()
            main_event.clear()
            main_event.wait()
        except Bot.ActionsAreOver:
            playerExecutor.bot.sleep_async(4)

        try:
            enemyExecuror.next_move()
            main_event.clear()
            main_event.wait()
        except Bot.ActionsAreOver:
            enemyExecuror.bot.sleep_async(2)




if __name__ == "__main__":
    main()