from config import Config
from game import Game


def main():
    config = Config()
    game = Game(config)
    game.run()


main()
