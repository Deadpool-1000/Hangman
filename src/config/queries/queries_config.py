import logging
import os
import yaml
from functools import lru_cache
from pydantic_settings import BaseSettings

from src.config.env.settings import get_settings


logger = logging.getLogger('main.queries_config')

path_current_directory = os.path.dirname(__file__)
QUERIES_CONFIG_PATH = os.path.join(path_current_directory, 'queries.yml')
with open(QUERIES_CONFIG_PATH, 'r') as f:
    logger.info("loading queries.yml")
    data = yaml.safe_load(f)


settings = get_settings()


class QueriesConfig(BaseSettings):
    CREATE_TABLE_AUTH: str = data['CREATE_TABLE_AUTH']
    CREATE_TABLE_PLAYER: str = data['CREATE_TABLE_PLAYER']
    FIND_USER_QUERY: str = data['FIND_USER_QUERY']
    INSERT_INTO_AUTH: str = data['INSERT_INTO_AUTH']
    INSERT_INTO_PLAYERS: str = data['INSERT_INTO_PLAYERS']
    INSERT_INTO_GAME_CONFIG: str = data['INSERT_INTO_GAME_CONFIG']
    PLAYER_DATA: str = data['PLAYER_DATA']
    UPDATE_HIGH_SCORE: str = data['UPDATE_HIGH_SCORE']
    GET_LEADERBOARD: str = data['GET_LEADERBOARD']
    UPDATE_PLAYER_STATS: str = data['UPDATE_PLAYER_STATS']
    CREATE_TABLE_QUERY: str = data['CREATE_TABLE_QUERY']
    GAME_CONFIG_QUERY: str = data['GAME_CONFIG_QUERY']
    USER_WITH_UNAME: str = data['USER_WITH_UNAME']
    UPDATE_PLAYER_SCORE: str = data['UPDATE_PLAYER_SCORE']
    GET_HIGH_SCORE: str = data['GET_HIGH_SCORE']
    UPDATE_GAME_CONFIG: str = data['UPDATE_GAME_CONFIG']
    DBPATH: str = os.path.join(path_current_directory, rf'..\..\..\{data["DBPATH"]}')


class TestingEnvironment(QueriesConfig):
    DBPATH: str = os.path.join(path_current_directory, rf'..\..\..\tests\data\hangman_test.db')


@lru_cache
def get_queries_config():
    if settings.run_env == 'TEST':
        return TestingEnvironment()
    else:
        return QueriesConfig()
