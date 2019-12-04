from dataclasses import dataclass
from threading import Event
from time import sleep

from engine.runner.executor import Executor
from engine.gameobjects.bots.bot import Bot
from bots_code.code import *

@dataclass
class Game:
    def start(self):
        # used to lock main Thread
        main_event = Event()
        executors = []
        playerExecutor  = Executor(Bot(0, 'player', main_event), run_user)
        enemyExecuror   = Executor(Bot(0, 'enemy',  main_event), run_enemy)
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

    def stop(self):
        pass

    def update(self):
        pass

def main():
    game = Game()
    game.start()

if __name__ == '__main__':
    main()