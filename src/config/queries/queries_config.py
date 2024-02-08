import os
from functools import lru_cache

import yaml
from pydantic_settings import BaseSettings

path_current_directory = os.path.dirname(__file__)
QUERIES_CONFIG_PATH = os.path.join(path_current_directory, 'queries.yml')
with open(QUERIES_CONFIG_PATH, 'r') as f:
    print("loading queries.yml")
    data = yaml.safe_load(f)


class QueriesConfig(BaseSettings):
    CREATE_TABLE_AUTH: str = data['CREATE_TABLE_AUTH']
    CREATE_TABLE_PLAYER: str = data['CREATE_TABLE_PLAYER']
    FIND_USER_QUERY: str = data['FIND_USER_QUERY']
    INSERT_INTO_AUTH: str = data['INSERT_INTO_AUTH']
    INSERT_INTO_PLAYERS: str = data['INSERT_INTO_PLAYERS']
    PLAYER_DATA: str = data['PLAYER_DATA']
    UPDATE_HIGH_SCORE: str = data['UPDATE_HIGH_SCORE']
    GET_LEADERBOARD: str = data['GET_LEADERBOARD']
    UPDATE_PLAYER_STATS: str = data['UPDATE_PLAYER_STATS']
    CREATE_TABLE_QUERY: str = data['CREATE_TABLE_QUERY']
    GAME_CONFIG_QUERY: str = data['GAME_CONFIG_QUERY']
    USER_WITH_UNAME: str = data['USER_WITH_UNAME']
    UPDATE_PLAYER_SCORE: str = data['UPDATE_PLAYER_SCORE']
    GET_HIGH_SCORE: str = data['GET_HIGH_SCORE']
    DBPATH: str = os.path.join(path_current_directory, rf'..\..\..\{data["DBPATH"]}')


@lru_cache
def get_queries_config():
    return QueriesConfig()
