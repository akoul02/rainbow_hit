from dataclasses import dataclass
from threading import Event
from time import sleep

from engine.runner.executor import Executor
from engine.gameobjects.bots.bot import Bot
from bots_code.code import *
from constants import MAX_STEPS
from exceptions import ActionsAreOver

@dataclass
class Game:
    def start(self):
        # used to lock main Thread
        main_event = Event()
        executors = [
            Executor(Bot(0, 'player', main_event), MAX_STEPS, run_user), 
            Executor(Bot(0, 'enemy',  main_event), MAX_STEPS, run_enemy),
            Executor(Bot(0, 'enemy2', main_event), MAX_STEPS, run_enemy2)
        ]

        for step in range(0, MAX_STEPS):
            print(f'\nStep: {step}')
            for executor in executors:
                try:
                    executor.next_move(step)
                except ActionsAreOver:
                    executor.bot.sleep(blocking=False)

    def stop(self):
        pass

    def update(self):
        pass

def main():
    game = Game()
    game.start()

if __name__ == '__main__':
    main()