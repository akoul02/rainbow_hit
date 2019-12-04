from threading import Event
from executor import Executor
from playerCode import *
from time import sleep
from bot import Bot

def main():
    # used to lock main Thread
    main_event = Event()
    executors = []
    playerExecutor  = Executor(Bot(0, 'player', main_event), run_user)
    enemyExecuror   = Executor(Bot(0, 'enemy', main_event),  run_enemy)
    enemyExecuror2  = Executor(Bot(0, 'enemy2', main_event), run_enemy2)

    for step in range(1, 20):
        print(f'\nStep: {step}')
        try:
            playerExecutor.next_move()
        except Bot.ActionsAreOver:
            playerExecutor.bot.sleep(blocking=False)

        try:
            enemyExecuror.next_move()
        except Bot.ActionsAreOver:
            enemyExecuror.bot.sleep(blocking=False)

        try:
            enemyExecuror2.next_move()
        except Bot.ActionsAreOver:
            enemyExecuror2.bot.sleep(blocking=False)


if __name__ == "__main__":
    main()