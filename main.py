import logging
from src.game.game import Game
from src.config.helper import load_config

# Logging configuration
logging.basicConfig(format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
                    datefmt="%d-%M-%Y %H:%M:%S", level=logging.DEBUG, filename='src/utils/logs.log')
logger = logging.getLogger("main")


def entry_point(f):
    if f.__module__ == '__main__':
        f()
    return f


@entry_point
@load_config
def main():
    logger.info('Game Started')
    Game.start_menu()
    logger.info('Game Ended')
