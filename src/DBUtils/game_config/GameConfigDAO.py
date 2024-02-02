import sqlite3

from src.config.queries.queries_config import QueriesConfig


class GameConfigDAO:
    singleton = 1
    """
    Performs DB read operations on Game configurations.
    Can be used as context manager
    """

    def __init__(self, conn):
        self.cur = conn.cursor()
        if self.singleton != 0:
            self.cur.execute(QueriesConfig.CREATE_TABLE_QUERY)
            conn.commit()
            self.singleton -= 1

    def get_game_params(self, param) -> list[(sqlite3.Cursor, sqlite3.Cursor)]:
        rws = self.cur.execute(QueriesConfig.GAME_CONFIG_QUERY, (param,))
        return [(row[2], row[3]) for row in rws.fetchall()]

    def get_round_options(self) -> list[sqlite3.Cursor]:
        return self.get_game_params("ROUND")

    def get_difficulty_options(self) -> list[sqlite3.Cursor]:
        return self.get_game_params("DIFFICULTY")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_tb or exc_val:
            # re raises error on the callers side
            return False
        self.connection.commit()
        self.connection.close()
