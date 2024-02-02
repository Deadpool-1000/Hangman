import sqlite3

from src.DBUtils.players.PlayerDAO import PlayerDAO
from src.handlers.base_handler.base_handler import BaseHandler
from src.DBUtils.database.database import Database
from src.utils.exception import ApplicationError


class SignupHandler(BaseHandler):
    def __init__(self, db: Database, username: str, password: str):
        super().__init__(db)
        self.username = username
        self.password = password

    def signup(self):
        try:
            with PlayerDAO(self.db.connection) as p_dao:
                p_dao.add_user_details(self.username, self.password)
                return True

        except sqlite3.IntegrityError as e:
            raise ApplicationError(code=409, message='Username taken.')