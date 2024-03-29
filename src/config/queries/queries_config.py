import yaml
import os

path_current_directory = os.path.dirname(__file__)
QUERIES_CONFIG_PATH = os.path.join(path_current_directory, 'queries.yml')


class QueriesConfig:
    CREATE_TABLE_AUTH = None
    CREATE_TABLE_PLAYER = None
    FIND_USER_QUERY = None
    INSERT_INTO_AUTH = None
    INSERT_INTO_PLAYERS = None
    PLAYER_DATA = None
    UPDATE_HIGH_SCORE = None
    GET_LEADERBOARD = None
    UPDATE_PLAYER_STATS = None
    CREATE_TABLE_QUERY = None
    GAME_CONFIG_QUERY = None
    USER_WITH_UNAME = None
    UPDATE_PLAYER_SCORE = None
    GET_HIGH_SCORE = None
    DBPATH = None

    @classmethod
    def load(cls):
        with open(QUERIES_CONFIG_PATH, 'r') as f:
            data = yaml.safe_load(f)
            cls.CREATE_TABLE_AUTH = data['CREATE_TABLE_AUTH']
            cls.CREATE_TABLE_PLAYER = data['CREATE_TABLE_PLAYER']
            cls.FIND_USER_QUERY = data['FIND_USER_QUERY']
            cls.INSERT_INTO_AUTH = data['INSERT_INTO_AUTH']
            cls.INSERT_INTO_PLAYERS = data['INSERT_INTO_PLAYERS']
            cls.PLAYER_DATA = data['PLAYER_DATA']
            cls.UPDATE_HIGH_SCORE = data['UPDATE_HIGH_SCORE']
            cls.GET_LEADERBOARD = data['GET_LEADERBOARD']
            cls.UPDATE_PLAYER_STATS = data['UPDATE_PLAYER_STATS']
            cls.CREATE_TABLE_QUERY = data['CREATE_TABLE_QUERY']
            cls.GAME_CONFIG_QUERY = data['GAME_CONFIG_QUERY']
            cls.USER_WITH_UNAME = data['USER_WITH_UNAME']
            cls.UPDATE_PLAYER_SCORE = data['UPDATE_PLAYER_SCORE']
            cls.GET_HIGH_SCORE = data['GET_HIGH_SCORE']
            cls.DBPATH = data['DBPATH']
