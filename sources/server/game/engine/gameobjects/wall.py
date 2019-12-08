from dataclasses import dataclass

from engine.gameobjects.destroyable import Destroyable

@dataclass
class Wall(Destroyable):
    '''Object, that represents killable wall
    '''
    pass
