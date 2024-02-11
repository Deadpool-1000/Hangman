import sqlite3

from src.config import get_queries_config

queries_config = get_queries_config()


class GameParamsDAO:
    """
    Performs DB read operations on Game configurations.
    Can be used as context manager
    """

    def __init__(self, conn):
        self.cur = conn.cursor()

    def get_game_params(self, param) -> list[(sqlite3.Cursor, sqlite3.Cursor)]:
        rws = self.cur.execute(queries_config.GAME_CONFIG_QUERY, (param,))
        return [(dict(row)['config_key'], dict(row)['config_value']) for row in rws.fetchall()]

    def get_round_options(self) -> list[sqlite3.Cursor]:
        return self.get_game_params("ROUND")

    def get_difficulty_options(self):
        return self.get_game_params("DIFFICULTY")

    def update_game_params(self, game_params):
        self.cur.executemany(queries_config.UPDATE_GAME_CONFIG, game_params)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()
        if exc_type or exc_tb or exc_val:
            # re raises error on the callers side
            return False
