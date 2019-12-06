from dataclasses import dataclass
from threading import Event
from time import sleep

from engine.gameobjects.game_world import World
from engine.runner.executor import Executor
from engine.gameobjects.bots.bot import Bot
from constants import MAX_STEPS
from exceptions import ActionsAreOver
from bots_code.code import *

@dataclass
class Game:
    '''Base game class.
    '''
    def start(self):
        '''Starts the game

        Returns
        -------
        None
        '''
        # used to lock main Thread
        main_event = Event()
        executors = [
            Executor(Bot(0, 0, 'player', main_event), MAX_STEPS, run_user), 
            Executor(Bot(0, 0, 'enemy',  main_event), MAX_STEPS, run_enemy),
            Executor(Bot(0, 0, 'enemy2', main_event), MAX_STEPS, run_enemy2)
        ]

        for step in range(0, MAX_STEPS):
            print(f'\nStep: {step}')
            for executor in executors:
                try:
                    executor.next_move(step)
                except ActionsAreOver:
                    executor.bot.sleep(blocking=False)

    def stop(self):
        '''Stops the game

        Returns
        -------
        None
        '''

    def update(self):
        pass

def main():
    game = Game()
    game.start()

if __name__ == '__main__':
    main()