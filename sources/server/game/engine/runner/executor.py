from dataclasses import *
from server.game.constants import THREAD_TIMEOUT
from server.game.engine.gameobjects.bots.bot import Bot
from server.game.engine.utils.kthread import KThread
from server.game.exceptions import *
from threading import Thread, Event
from typing import Callable


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

    thread: KThread = field(default_factory=KThread)
    is_started: bool = False

    def __post_init__(self):
        self.thread = KThread(target=self.run_func, args=[self.bot])

    def next_move(self):
        '''continues execution
        Raises
        ------
        ActionsAreOver
            Raises, if actions inside "user-code" are over

        BotTimeoutError
            Raises, if bot thread runs for very long 
            time (longer than BotTimeoutError)
        
        ThreadKilledError
            Raises, if thread was killed at sopme point
        '''
        if not self.thread.killed:
            # if bot in thread is alive
            if self.bot.is_alive():
                if not self.is_started:
                    self.is_started = True
                    self.thread.start()
                    self.bot.event.set()
                else:
                    if self.thread.is_alive():
                        # if thread is alive (actions are still available)
                        self.bot.event.set()
                    else:
                        # if actions are over
                        self.thread.join()
                        raise ActionsAreOver()

                # clear main event
                self.bot.main_event.clear()
                # wait here, while bot is doing his actions
                timeout = self.bot.main_event.wait(THREAD_TIMEOUT)

                if not timeout:
                    # timeout over, but bot thread is still running
                    self.thread.terminate(BotTimeoutError)
                    self.bot.main_event.set()
                    raise BotTimeoutError()
            else:
                # if bot is dead
                if self.thread.is_alive():
                    self.bot.event.set()
                    self.thread.terminate(BotIsDead)
                    self.bot.main_event.set()
                raise BotIsDead()
        else:
            self.bot.main_event.clear()
            raise ThreadKilledError()
