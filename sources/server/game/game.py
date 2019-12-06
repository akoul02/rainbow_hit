from dataclasses import dataclass
from threading import Event
from time import sleep

from engine.runner.executor import Executor
from engine.gameobjects.bots.bot import Bot
from bots_code.code import *
from constants import MAX_STEPS
from exceptions import ActionsAreOver
from engine.gameobjects.game_world import World

@dataclass
class Game:
    def start(self):
        # used to lock main Thread
        main_event = Event()
        game_world = World()
        # executors = [
        #     Executor(Bot(0, 0, 'player', main_event), MAX_STEPS, run_user), 
        #     Executor(Bot(0, 0, 'enemy',  main_event), MAX_STEPS, run_enemy),
        #     Executor(Bot(0, 0, 'enemy2', main_event), MAX_STEPS, run_enemy2)
        # ]
        player_exec = Executor(Bot(0, 0, 'player', main_event, game_world, ), MAX_STEPS, run_user)
        enemy_exec  = Executor(Bot(0, 0, 'enemy',  main_event, game_world, ), MAX_STEPS, run_enemy)
        enemy_exec2 = Executor(Bot(0, 0, 'enemy2', main_event, game_world, ), MAX_STEPS, run_enemy2)

        for step in range(0, MAX_STEPS):
            print(f'\nStep: {step}')
            try:
                player_exec.next_move(step)
            except ActionsAreOver:
                player_exec.bot.sleep(blocking=False)

            try:
                enemy_exec.next_move(step)
            except ActionsAreOver:
                enemy_exec.bot.sleep(blocking=False)

            try:
                enemy_exec2.next_move(step)
            except ActionsAreOver:
                enemy_exec2.bot.sleep(blocking=False)
            # for executor in executors:
            #     try:
            #         executor.next_move(step)
            #     except ActionsAreOver:
            #         executor.bot.sleep(blocking=False)

    def stop(self):
        pass

    def update(self):
        pass

def main():
    game = Game()
    game.start()

if __name__ == '__main__':
    main()