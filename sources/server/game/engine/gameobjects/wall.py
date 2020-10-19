from dataclasses import dataclass

from server.game.engine.gameobjects.destroyable import Destroyable
from server.game.engine.utils.point import Point


@dataclass
class Wall(Destroyable):
    '''Object, that represents killable wall
    '''

    def serialize(self):
        return f'"({self.coord.x}, {self.coord.y})": ["Wall", "{self.name}", {self.health}]'

    name: str = 'Wall'

    def current_location(self) -> Point:
        '''Get current location as point

        Returns
        -------
        point : Point
            current coordinates
        '''
        return Point(self.coord.x, self.coord.y)
