import logging
import sqlite3

from src.DBUtils.database import Database
from src.utils.exception import DatabaseException

logger = logging.getLogger('main.base_handler')


class BaseHandler:
    def __init__(self, db: Database):
        self.db = db

    def __enter__(self):
        try:
            self.db.connect()

        except sqlite3.Error:
            logger.error('There was a problem connecting to database')
            raise DatabaseException('There was a problem connecting to database')

        else:
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()
        if exc_type or exc_tb or exc_val:
            return False
