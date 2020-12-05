import traceback

from .bots_code import config
from .bots_code.code_sync import BotActivityWrapper, get_bot_activity
from .engine.gameobjects.game_world import World
from .constants import MAX_STEPS, INIT_WORLD_CMD, GAME_OVER, LABYRINTH_DENSITY, BOTS_STATE
from .engine.gameobjects.bots.bot_sync import Bot
from .engine.utils.point import Point
from .exceptions import GameOver, BotIsDead


class Game:
    def __init__(self,
                 player1=None,
                 player2=None,
                 names=['player1', 'player2']):
        self.result = False
        self.history = open('history.json', 'w')
        self.world = World.generate('pvp', LABYRINTH_DENSITY)

        self.bots = [
            BotActivityWrapper(
                Bot(Point(0, 0), self.world, 10, 10, True, names[0]), player1
                or get_bot_activity(config.p1sc)),
            BotActivityWrapper(
                Bot(Point(15, 15), self.world, 10, 10, True, names[1]), player2
                or get_bot_activity(config.p2sc))
        ]

        self.__save_map()

    def __del__(self):
        self.history.close()

    def __save_map(self):
        objects = ''
        for idx in range(len(self.world.objects)):
            obj = self.world.objects[idx]

            if idx == len(self.world.objects) - 1:
                objects += ' ' * 8 + obj.serialize()
            else:
                objects += ' ' * 8 + obj.serialize() + ',\n'

        self.history.write('[' + INIT_WORLD_CMD.format(objects) + ',\n')
        self.history.flush()

    def make_step(self, bot):
        try:
            action = bot.make_step()
            self.world.update()
        except BotIsDead:
            action = bot.sleep()
        except GameOver as e:
            return e
        except Exception as e:
            print(f'Received {e.__repr__()} while executing {bot.name} script.')
            if config.print_traceback:
                traceback.print_exc()
            action = bot.sleep()
        finally:
            self.history.write(action + ',\n')
            self.history.flush()
            self.history.write(BOTS_STATE.format(bot.name, bot.current_hp()) + ',\n')
            self.history.flush()

    def run(self):
        for _step in range(0, MAX_STEPS):
            for bot in self.bots:
                state = self.make_step(bot)
                if state is not None:
                    return state
        return GameOver(False)

    def start_game_loop(self):
        result = False
        winner = None
        for step in range(0, MAX_STEPS):
            for bot in self.bots:
                state = self.make_step(bot)
                if state is not None:
                    result = state.game_won
                    winner = state.winner.name
                    break
            if result:
                break

        if result:
            self.history.write(GAME_OVER.format(winner, "false" if result else "true") + ']')
            self.history.flush()
            print(f'Winner is: {winner}')
        else:
            self.history.write(GAME_OVER.format('', "false" if result else "true") + ']')
            self.history.flush()
            print(f'Draw!')

        print('Simulation is over!')

        return result
