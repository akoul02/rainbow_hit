from threading import Thread, Event
from typing import Callable
from exceptions import ActionsAreOver

from engine.gameobjects.bots.bot import Bot

class Executor:
    bot: Bot
    max_steps: int
    run_func: Callable[[Bot], None]

    thread: Thread
    is_started: bool = False
        
    def __init__(self, bot: Bot, max_steps: int, run_func: Callable[[Bot], None]):
        self.bot = bot
        self.max_steps = max_steps
        self.run_func = run_func

        self.thread = Thread(target=self.run_func, args=[self.bot])

    def next_move(self, n: int):
        '''
        Parameters
        ----------
        n : int
            Current step number

        Raises
        ------
        Bot.ActionsAreOver
            Raises, if actions inside "user-code" are over
        '''
        if not self.is_started:
            self.is_started = True
            self.thread.start()
            self.bot.event.set()
        else:
            if self.thread.is_alive():
                self.bot.event.set()
            else:
                self.thread.join()
                raise ActionsAreOver()
        
        self.bot.main_event.clear()
        # wait here, while the bot does it actions
        self.bot.main_event.wait()
