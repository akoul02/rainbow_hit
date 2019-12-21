import sys, os
sys.path.insert(0, os.path.dirname(__file__) + '/client/')
sys.path.insert(0, os.path.dirname(__file__) + '/server/game/')

from client.main import Client
from server.game.game import Game
from server.game.constants import TRACE_NAME

def run():
    game = Game()
    game.start()

    client = Client(TRACE_NAME)
    client.creating_game_objects()
    client.main_loop()

def main():
    run()

if __name__ == "__main__":
    main()