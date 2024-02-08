import sqlite3

from src.config import get_queries_config

queries_config = get_queries_config()


# TODO can also make this class Abstract
class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        print(f"Connecting to {queries_config.DBPATH}..........")
        self.connection = sqlite3.connect(queries_config.DBPATH)
        self.connection.row_factory = sqlite3.Row

    def close(self):
        self.connection.commit()
        self.connection.close()
