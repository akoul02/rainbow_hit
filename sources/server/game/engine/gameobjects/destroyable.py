from dataclasses import dataclass
from server.game.engine.utils.math_utils import clamp
from server.game.engine.gameobjects.gameobject import GameObject


@dataclass
class Destroyable(GameObject):
    '''Base class, that describe "destroyable" object

    Attributes
    ----------
    health : int
        Current object health

    max_health : int
        Max possible health

    alive : bool
        Shows, object status (dead/alive)
    '''
    health: int
    max_health: int
    alive: bool

    def reduce_health(self, n: int) -> int:
        '''Decrease hp for n points. Resulting value clamps between 0 and max_health

        Parameters
        ----------
        n : int
            damage points
        '''
        self.health = clamp(self.health - n, 0, self.max_health)
        return self.health

    def increase_health(self, n: int) -> int:
        '''Increase hp for n points. Resulting value clamps between 0 and max_health

        Parameters
        ----------
        n : int
            heal points
        '''
        self.health = clamp(self.health + n, 0, self.max_health)
        return self.health

    def is_alive(self) -> bool:
        '''Returns object status (alive/dead)
        '''
        return self.alive

    def kill(self) -> None:
        '''Kill current object.
        '''
        self.health = 0
        self.alive = False
        return None
