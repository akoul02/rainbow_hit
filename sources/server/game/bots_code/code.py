import random
import time
from collections import deque
from server.game.bots_code import bot_scripts
from server.game.engine.gameobjects.bots.bot import Bot
from server.game.engine.gameobjects.bots.user_bot import UserBot
from server.game.engine.gameobjects.destroyable import Destroyable
from server.game.engine.gameobjects.wall import Wall
from server.game.engine.utils.direction import Direction
from server.game.engine.utils.point import Point
from server.game.exceptions import *
from typing import Any, List


def continuemain(func):
    '''
    Decorator, that should be added automatically for any user-code
    First argument should be bot instance
    '''

    def wrapper(self, *args, **kwargs):
        try:
            self.main_event.set()

            # block current thread
            self.event.wait()
            self.event.clear()
            ret = func(self, *args, **kwargs)
            return ret
        except (StepsAreOver, ActionsAreOver, BotTimeoutError, BotIsDead) as e:
            # handle async-raised exceptions
            return e
        finally:
            # allow main thread to continue
            if isinstance(self, Bot):
                self.main_event.set()
            else:
                raise InvalidSelfInstance('Object type mismatch! Should be Bot().')

    return wrapper


def get_callable_script(name):
    return __import__(f'server.game.bots_code.bot_scripts.{name}', fromlist=[name]).perform
