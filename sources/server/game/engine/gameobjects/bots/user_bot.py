from dataclasses import dataclass

from server.game.engine.gameobjects.bots.bot_sync import Bot


@dataclass
class UserBot(Bot):
    '''Basic class for player bot
    '''
    pass
