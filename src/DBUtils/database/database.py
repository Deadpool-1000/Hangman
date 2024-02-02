import sqlite3
from src.config.queries.queries_config import QueriesConfig


# TODO can also make this class Abstract
class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(QueriesConfig.DBPATH)
        self.connection.row_factory = sqlite3.Row

    def close(self):
        self.connection.commit()
        self.connection.close()
