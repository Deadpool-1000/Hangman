import logging
from config.config import Config
from Game import Game


# Logging configuration
logging.basicConfig(format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
                    datefmt="%d-%M-%Y %H:%M:%S", level=logging.DEBUG, filename='logs.log')
logger = logging.getLogger("main")


if __name__ == "__main__":
    # Load all the configurations
    Config.load()
    # Start the menu
    Game.start_menu()
