from exceptions import ActionsAreOver
from threading import Thread, Event
from dataclasses import *
from typing import Callable

from engine.gameobjects.bots.bot import Bot

@dataclass
class Executor:
    '''Executor class. It executes user-code in strict sequnce.

    Attributes
    ----------
    bot : Bot
        pointer to bot object, associated with code

    max_steps : int
        max possible steps, that can be be performed

    run_func : Callable[[Bot], None]
        function, where user-code is defined

    thread : Thread
        thread, where all user-code is running

    is_started : bool
        boolean flag, that shows, if thread was already started
    '''
    bot: Bot
    max_steps: int
    run_func: Callable[[Bot], None]

    thread: Thread = Thread(target=run_func, args=[bot])
    is_started: bool = False

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
