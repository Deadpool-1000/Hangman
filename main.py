import logging
from config.prompt import PromptConfig
from config.utils_config import UtilsConfig
from config.queries_config import QueriesConfig
from config.game_config import GameConfig
from config.words_config import WordsConfig
from config.hangman_config import HangmanConfig
from config.leaderboard_config import LeaderBoardConfig
from config.logs_config import LogsConfig
from config.user_config import UserConfig
from Game import Game


# Logging configuration
logging.basicConfig(format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
                    datefmt="%d-%M-%Y %H:%M:%S", level=logging.DEBUG, filename='logs.log')
logger = logging.getLogger("main")


if __name__ == "__main__":
    # Load all the configurations
    PromptConfig.load()
    UtilsConfig.load()
    QueriesConfig.load()
    GameConfig.load()
    WordsConfig.load()
    HangmanConfig.load()
    LeaderBoardConfig.load()
    LogsConfig.load()
    UserConfig.load()

    # Start the menu
    Game.start_menu()
