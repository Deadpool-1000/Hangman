import logging
import sqlite3

from src.DBUtils import Database, PlayerDAO
from src.handlers import BaseHandler
from src.utils.exception import DatabaseException

logger = logging.getLogger('main.user_controller')


class UserHandler(BaseHandler):
    def __init__(self, db: Database, identity):
        super().__init__(db)
        self.identity = identity

    def get_profile(self):
        try:
            with PlayerDAO(self.db.connection) as p_dao:
                user = p_dao.get_user_details(self.identity)
            return user

        except sqlite3.Error as e:
            logger.error(f"Database error while fetching profile {e}")
            raise DatabaseException('There was some problem while fetching your profile.')
