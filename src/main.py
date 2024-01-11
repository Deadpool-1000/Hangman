import os
import logging
from src.game.game import Game
from src.config.helper import load_config

path_current_directory = os.path.dirname(__file__)
LOG_FILE_PATH = os.path.join(path_current_directory, 'utils/logs.log')

# Logging configuration
logging.basicConfig(format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
                    datefmt="%d-%M-%Y %H:%M:%S", level=logging.DEBUG, filename=LOG_FILE_PATH)
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
