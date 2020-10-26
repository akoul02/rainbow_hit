from client.main import Client
from server.game.constants import TRACE_NAME
from server.game.game_sync import Game
import sys


def run():
    print(f'[DEBUG] Python {sys.version.split()[0]}')

    game = Game()
    game.start_game_loop()

    client = Client(TRACE_NAME)
    client.creating_game_objects()
    client.main_loop()


def main():
    run()


if __name__ == "__main__":
    main()
