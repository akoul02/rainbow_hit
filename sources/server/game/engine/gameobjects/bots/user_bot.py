from dataclasses import dataclass

from server.game.engine.gameobjects.bots.bot import Bot


@dataclass
class UserBot(Bot):
    '''Basic class for player bot
    '''
    pass
