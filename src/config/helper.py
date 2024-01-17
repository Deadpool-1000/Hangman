from src.config.queries.queries_config import QueriesConfig
from src.config.words.words_config import WordsConfig
from src.config.logs.logs_config import LogsConfig
from src.config.user.user_config import UserConfig
from src.config.api.api_config import ApiConfig


def load_configurations():
    QueriesConfig.load()
    WordsConfig.load()
    LogsConfig.load()
    UserConfig.load()
    ApiConfig.load()


load_configurations()
