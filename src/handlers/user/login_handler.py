import hashlib
import logging
import sqlite3

from src.DBUtils import Database, PlayerDAO
from src.handlers import BaseHandler
from src.utils.exception import ApplicationError, DatabaseException

logger = logging.getLogger('main.login_handler')


class LoginHandler(BaseHandler):
    def __init__(self, db: Database, username: str, password: str):
        super().__init__(db)
        self.username = username
        self.password = password

    def login(self):
        try:
            with PlayerDAO(self.db.connection) as p_dao:
                found_user = p_dao.find_user_with_uname(self.username)

                if len(found_user) == 0:
                    logger.debug(f"Invalid Username {self.username}")
                    raise ApplicationError(
                        code=401,
                        message="Username or password Incorrect."
                    )

                found_user = found_user[0]

                # Invalid password
                if found_user['password'] != hashlib.sha256(self.password.encode()).hexdigest():
                    logger.debug(f"Invalid password for username {self.username}")
                    raise ApplicationError(
                        code=401,
                        message="Username or password Incorrect."
                    )

                return found_user

        except sqlite3.Error:
            logger.error(f'There was some problem connecting to database')
            raise DatabaseException('There was some problem while logging in.')
