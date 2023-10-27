import sqlite3
from config.config import Config

CREATE_TABLE_QUERY = "CREATE TABLE IF NOT EXISTS game_config(config_id INTEGER PRIMARY KEY AUTOINCREMENT, config_name TEXT, config_key TEXT, config_value INTEGER)"
GAME_CONFIG_QUERY = "SELECT * FROM game_config WHERE config_name=?"


class GameConfigDAO:
    singleton = 1

    def __init__(self):
        self.connection = sqlite3.connect(Config.DBPATH)
        self.cur = self.connection.cursor()
        if self.singleton != 1:
            self.cur.execute(CREATE_TABLE_QUERY)
            self.connection.commit()
            self.singleton -= 1

    def get_game_params(self, param):
        rws = self.cur.execute(GAME_CONFIG_QUERY, (param,))
        return [row[3] for row in rws.fetchall()]

    def get_round_options(self):
        return self.get_game_params("ROUND")

    def get_difficulty_options(self):
        return self.get_game_params("LENGTH")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_tb or exc_val:
            # re raises error on the callers side
            return False
        self.connection.commit()
        self.connection.close()
