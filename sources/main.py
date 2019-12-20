import sys, os
sys.path.insert(0, os.path.dirname(__file__) + '/client/')
sys.path.insert(0, os.path.dirname(__file__) + '/server/game/')

from client.main import Client
from server.game.game import Game

def main():
    game = Game()
    game.start()

    client = Client()
    client.creating_game_objects()
    client.actions()




if __name__ == "__main__":
    main()