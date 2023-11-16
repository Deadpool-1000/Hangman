from functools import wraps
from src.config.utils.utils_config import UtilsConfig
from src.config.queries.queries_config import QueriesConfig
from src.config.game.game_config import GameConfig
from src.config.words.words_config import WordsConfig
from src.config.hangman.hangman_config import HangmanConfig
from src.config.leaderboard.leaderboard_config import LeaderBoardConfig
from src.config.logs.logs_config import LogsConfig
from src.config.user.user_config import UserConfig
from src.config.prompts.prompts_config import PromptConfig


def load_config(func):
    @wraps(func)
    def inner(*args):
        PromptConfig.load()
        UtilsConfig.load()
        QueriesConfig.load()
        GameConfig.load()
        WordsConfig.load()
        HangmanConfig.load()
        LeaderBoardConfig.load()
        LogsConfig.load()
        UserConfig.load()
        func()
    return inner
