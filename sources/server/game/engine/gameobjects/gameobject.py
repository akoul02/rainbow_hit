from dataclasses import dataclass

@dataclass
class GameObject:
    '''Generic class for all game-objects. 
    Any kind of game-objects should be inherited from this class.

    Attributes
    ----------
    x : int
        x-axis coordinate
    
    y : int
        y-axis coordinate
    '''

    def __init__(self):
        super().__init__()

    x: int
    y: int
