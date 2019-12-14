from dataclasses import dataclass
from threading import Event
from time import sleep

from engine.gameobjects.game_world import World
from engine.runner.executor import Executor
from engine.gameobjects.bots.bot import Bot
from engine.gameobjects.bots.enemy_bot import EnemyBot
from engine.gameobjects.bots.user_bot import UserBot
from engine.utils.point import Point
from constants import MAX_STEPS, BOT_DEFAULT_HP
from exceptions import ActionsAreOver, BotTimeoutError, StepsAreOver, ThreadKilledError, GameOver, BotIsDead
from bots_code.code import *

@dataclass
class Game:
    '''Base game class.
    '''
    def start(self) -> bool:
        '''Starts the game

        Returns
        -------
        None
        '''
        result: bool = False

        # used to lock main Thread
        main_event = Event()
        game_world = World('pvp')
        executors = [
            Executor(UserBot(Point(1, 1), game_world, 1, 10, True, 'player1', main_event), MAX_STEPS, run_enemy2), 
            Executor(UserBot(Point(2, 1), game_world, 1, 10, True, 'player2', main_event), MAX_STEPS, run_enemy3),
        ]

        try:
            # main game loop
            for step in range(0, MAX_STEPS):
                print(f'\nStep: {step}')
                for executor in executors:
                    try:
                        executor.next_move()
                        game_world.update()
                    except (ActionsAreOver, BotTimeoutError, ThreadKilledError) as e:
                        print(f'Exception message: {e} [{executor.bot.name}]')
                        executor.bot.sleep(blocking=False)
        except GameOver as e:
            result = e.game_won
            winner = e.winner.name
        finally:
            for executor in executors:
                executor.bot.event.set()
                executor.thread.terminate(StepsAreOver)
        if result:
            print(f'Winner is: {winner}')
        else:
            print(f'Draw!')
        
        print('Simulation is over!')

        return result

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
    result = game.start()

if __name__ == '__main__':
    main()
