from dataclasses import dataclass

@dataclass
class GameObject:
    '''Generic class for all game-objects. 
    Any kind of game-objects should be inherited from this class.

    Attributes
    ----------
    x : float
        x-axis coordinate
    
    y : float
        y-axis coordinate
    '''
    x: float
    y: float
