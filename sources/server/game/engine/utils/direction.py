import enum

class Direction(enum.Enum):
    '''Describes all possible directions.
    '''
    North     = N  = Up        = 1
    NorthEast = NE = RightUp   = UpRight   = 2
    East      = E  = Right     = 3
    SouthEast = SE = DownRight = RightDown = 4
    South     = S  = Down      = 5 
    SouthWest = SW = LeftDown  = DownLeft  = 6
    West      = W  = Left      = 7 
    NorthWest = NW = LeftUp    = UpLeft    = 8

    def get_coords(self):
        '''
        Returns
        -------
        (x, y)
            tuple with x-axis and y-axis coordinate
        
        Examples:
        --------
        >>> d = Direction.RightDown
        >>> d.get_coords()
        (1, -1)
        '''
        if self == self.N:
            return (0, 1)
        elif self == self.NE:
            return (1, 1)
        elif self == self.E:
            return (1, 0)
        elif self == self.SE:
            return (1, -1)
        elif self == self.S:
            return (0, -1)
        elif self == self.SW:
            return (-1, -1)
        elif self == self.W:
            return (-1, 0)
        elif self == self.NW:
            return (-1, 1)

    # overloading '~' operator
    def __invert__(self):
        '''Inverts direction
        
        Returns
        -------
        dir : Direction

        Examples
        --------
        >>> ~Direction.Up
        <Direction.South: 5>
        
        '''
        if self == self.N:
            return self.S
        elif self == self.NE:
            return self.SW
        elif self == self.E:
            return self.W
        elif self == self.SE:
            return self.NW
        elif self == self.S:
            return self.N
        elif self == self.SW:
            return self.NE
        elif self == self.W:
            return self.E
        elif self == self.NW:
            return self.SE
