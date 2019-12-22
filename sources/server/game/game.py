from dataclasses import dataclass
from threading import Event
from time import sleep

from engine.gameobjects.game_world import World
from engine.runner.executor import Executor
from engine.gameobjects.bots.bot import Bot
from engine.gameobjects.bots.enemy_bot import EnemyBot
from engine.gameobjects.bots.user_bot import UserBot
from engine.utils.point import Point
from constants import MAX_STEPS, BOT_DEFAULT_HP, SLEEP_CMD, INIT_WORLD_CMD, GAME_OVER, LABYRINTH_DENSITY
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
        history = open('history.json', 'w')

        # used to lock main Thread
        main_event = Event()
        game_world = World.generate('pvp', LABYRINTH_DENSITY)
        
        executors = [
            Executor(UserBot(Point(0, 0), game_world, 10, 10, True, 'player1', main_event), MAX_STEPS, run_user1),
            Executor(UserBot(Point(15, 15), game_world, 10, 10, True, 'player2', main_event), MAX_STEPS, run_user2),
        ]

        objects = ''
        for idx in range(len(game_world.objects)):
            obj = game_world.objects[idx]

            if idx == len(game_world.objects) - 1:
                objects += ' ' * 8 + obj.serialize()
            else:
                objects += ' ' * 8 + obj.serialize() + ',\n'
        
        history.write('[' + INIT_WORLD_CMD.format(objects) + ',\n')
        history.flush()

        # send world layout and bots positions
        
        # game_world.draw()

        try:
            # main game loop
            for step in range(0, MAX_STEPS):
                # print(f'\nStep: {step}')
                for executor in executors:
                    try:
                        executor.next_move()
                        game_world.update()
                    except (ActionsAreOver, BotTimeoutError, ThreadKilledError) as e:
                        # print(f'Exception message: {e} [{executor.bot.name}]')
                        executor.bot.sleep(blocking=False)
                    except BotIsDead as e:
                        pass
                        # print(f'Exception message: {e} [{executor.bot.name}]')
                    finally:
                        # game_world.draw()
                        # print(executor.bot.last_action)
                        # send updated state to server
                        # for client in clients:
                        #     net.send(executor.last_action, client)
                        history.write(executor.bot.last_action + ',\n')
                        history.flush()
                        pass
        except GameOver as e:
            result = e.game_won
            winner = e.winner.name
        finally:
            for executor in executors:
                executor.bot.event.set()
                executor.thread.terminate(StepsAreOver)

        if result:
            history.write(GAME_OVER.format(winner, "false" if result else "true") + ']')
            history.flush()
            print(f'Winner is: {winner}')
        else:
            history.write(GAME_OVER.format('', "false" if result else "true") + ']')
            history.flush()
            print(f'Draw!')
        
        # send result

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
