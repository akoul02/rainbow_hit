from typing import Union

from server.game.bots_code.code_dummy import BotActivityDummy as BotActivity
from server.game.engine.utils.direction import Direction
from server.game.engine.utils.point import Point


class BotActivityWrapper:
    def __init__(self, bot: object,
                 activity: BotActivity.__class__):  # TODO make empty classes for correct type definition without cycle imports
        self.__bot = bot
        self.activity = activity(self)
        self.__action = None
        self.__improper_access = False

    def make_step(self):
        if self.__improper_access:
            raise PermissionError('make_step() is restricted from internal calling')
        try:
            self.__improper_access = True
            self.__action = None

            self.activity.perform()

            if not self.__verify():
                return self.__bot.sleep()
            else:
                return self.__action
        finally:
            self.__improper_access = False

    def sleep(self):
        if self.__improper_access:
            self.__action = self.__bot.sleep()
        else:
            return self.__bot.sleep()

    def step(self, direction: Direction):
        self.__action = self.__bot.step(direction)

    def shoot(self, obj: Union[Point, object]):
        self.__action = self.__bot.shoot(obj)

    def scan(self):
        return self.__bot.scan()

    def current_location(self):
        return self.__bot.current_location()

    def current_hp(self):
        return self.__bot.current_hp()

    def __verify(self):
        return self.__action is not None

    @property
    def name(self):
        return self.__bot.name


def get_bot_activity(name):
    try:
        return __import__(f'server.game.bots_code.bot_scripts_sync.{name}', fromlist=[name]).BotActivity
    except:
        raise KeyError(f'Invalid script: {name}')
