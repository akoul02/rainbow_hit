from dataclasses import dataclass
from threading import Event
from time import sleep

from engine.gameobjects.game_world import World
from engine.runner.executor import Executor
from engine.gameobjects.bots.bot import Bot
from engine.utils.point import Point
from constants import MAX_STEPS, BOT_DEFAULT_HP
from exceptions import ActionsAreOver, BotTimeoutError, StepsAreOver, ThreadKilledError
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
        game_world = World()
        executors = [
            Executor(Bot(Point(0, 0), 10, 10, True, 'player', main_event, game_world, 2), MAX_STEPS, run_user), 
            Executor(Bot(Point(0, 0), 10, 10, True, 'enemy',  main_event, game_world, 2), MAX_STEPS, run_enemy),
            Executor(Bot(Point(0, 0), 10, 10, True, 'enemy2', main_event, game_world, 2), MAX_STEPS, run_enemy2)
        ]

        for step in range(0, MAX_STEPS):
            print(f'\nStep: {step}')
            for executor in executors:
                try:
                    executor.next_move()
                    game_world.update()
                except (ActionsAreOver, BotTimeoutError, ThreadKilledError) as e:
                    print(f'Exception message: {e}')
                    executor.bot.sleep(blocking=False)
        else:
            for executor in executors:
                executor.bot.event.set()
                executor.thread.terminate(StepsAreOver)
        
        print('Simulation is over!')

        return None

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
