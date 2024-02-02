import hashlib
import logging
from sqlite3 import Connection
from datetime import datetime

import shortuuid

from src.config.logs.logs_config import LogsConfig
from src.config.queries.queries_config import QueriesConfig
from src.config.user.user_config import UserConfig
from src.utils.exception import AlreadyExistsError
from src.utils.exception import InvalidUsernameOrPasswordError

logger = logging.getLogger("main.database")


class PlayerDAO:
    singleton = 1
    """
    Performs DB operations on Players.
    Can be used as context managers
    """

    def __init__(self, connection: Connection):
        self.cur = connection.cursor()
        # Create table only once
        if self.singleton != 0:
            logger.info("Three tables are created")
            self.cur.execute(QueriesConfig.CREATE_TABLE_AUTH)
            self.cur.execute(QueriesConfig.CREATE_TABLE_PLAYER)
            connection.commit()
            self.singleton -= 1

    def find_user_with_userid(self, user_id: str):
        """ Finds a user in the database with given username """
        rws = self.cur.execute(QueriesConfig.FIND_USER_QUERY, (user_id,))
        # ((user_id, uname, password, role),)
        return rws.fetchall()

    def find_user_with_uname(self, uname: str):
        rws = self.cur.execute(QueriesConfig.USER_WITH_UNAME, (uname,))
        return [dict(r) for r in rws.fetchall()]

    def add_user_details(self, uname: str, password: str):
        user_id = "U" + shortuuid.ShortUUID().random(length=5)
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cur.execute(QueriesConfig.INSERT_INTO_AUTH, (user_id, uname, hashed_password, "player"))
        self.cur.execute(QueriesConfig.INSERT_INTO_PLAYERS, (user_id, datetime.now()))

    def update_high_score(self, user_id: str, new_high_score: float):
        self.cur.execute(QueriesConfig.UPDATE_HIGH_SCORE, (new_high_score, datetime.now(), user_id))

    def get_leaderboard(self):
        rws = self.cur.execute(QueriesConfig.GET_LEADERBOARD)
        return [dict(r) for r in rws.fetchall()]

    def update_player_stats(self, total_games_played: int, total_games_won: int, user_id: str):
        self.cur.execute(QueriesConfig.UPDATE_PLAYER_SCORE, (total_games_played, total_games_won, user_id))

    def get_user_details(self, user_id):
        rws = self.cur.execute(QueriesConfig.PLAYER_DATA, (user_id,))
        user_data = [dict(r) for r in rws.fetchall()][0]

        # ((user_id, uname, high_score, total_game, total_games_won, high_score_created_on),)
        return user_data

    def get_high_score(self, user_id):
        rws = self.cur.execute(QueriesConfig.GET_HIGH_SCORE, (user_id,))
        return rws.fetchall()[0][0]

    def is_admin(self, user_id) -> bool:
        user = self.find_user_with_userid(user_id)
        return user[0][3] == UserConfig.ADMIN

    def find_user_details(self, user_id):
        rws = self.cur.execute(QueriesConfig.PLAYER_DATA, (user_id,))
        return dict(rws.fetchone())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_tb or exc_val:
            # re raises error on the callers side
            return False
        self.cur.close()
