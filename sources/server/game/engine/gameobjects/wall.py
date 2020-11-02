from dataclasses import dataclass
from .destroyable import Destroyable
from ..utils.point import Point


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

    @property
    def x(self):
        return self.value.x

    @property
    def y(self):
        return self.value.y
