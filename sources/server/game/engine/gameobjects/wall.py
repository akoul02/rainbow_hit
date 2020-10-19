from dataclasses import dataclass
from server.game.engine.gameobjects.destroyable import Destroyable


@dataclass
class Wall(Destroyable):
    '''Object, that represents killable wall
    '''

    def serialize(self):
        return f'"({self.coord.x}, {self.coord.y})": ["Wall", "{self.name}", {self.health}]'

    name: str = 'Wall'
    pass
