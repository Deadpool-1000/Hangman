import sqlite3
import logging
import hashlib
from datetime import datetime
from src.config.prompts.prompts_config import PromptConfig
from src.utils.exception import AlreadyExistsError
from src.utils.exception import InvalidUsernameOrPasswordError
from src.utils.named_tuples import Player, Leaderboard
from src.config.logs.logs_config import LogsConfig
from src.config.queries.queries_config import QueriesConfig

logger = logging.getLogger("main.database")


class PlayerDAO:
    singleton = 1
    """
    Performs DB operations on Players.
    Can be used as context managers
    """
    def __init__(self):
        self.connection = sqlite3.connect(PromptConfig.DBPATH)
        self.cur = self.connection.cursor()
        # Create table only once
        if self.singleton != 0:
            logger.info("Three tables are created")
            self.cur.execute(QueriesConfig.CREATE_TABLE_AUTH)
            self.cur.execute(QueriesConfig.CREATE_TABLE_PLAYER)
            self.connection.commit()
            self.singleton -= 1

    def find_user(self, uname: str):
        """ Finds a user in the database with given username """
        rws = self.cur.execute(QueriesConfig.FIND_USER_QUERY, (uname,))
        return rws

    def signup(self, uname: str, password: str):
        # Already exists
        rws = self.find_user(uname)
        print()
        if rws.fetchall():
            logger.error(LogsConfig.ALREADY_EXIST_LOG)
            raise AlreadyExistsError(LogsConfig.ALREADY_EXIST_LOG)
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cur.execute(QueriesConfig.INSERT_INTO_AUTH, (uname, hashed_password, "player"))
        self.cur.execute(QueriesConfig.INSERT_INTO_PLAYERS, (uname, datetime.now()))

    def login(self, uname: str, password: str):
        rws = self.find_user(uname)
        player = rws.fetchall()
        # Invalid Username
        if not player:
            logger.debug(LogsConfig.INVALID_USERNAME_OR_PASSWORD)
            logger.debug('Invalid Username')
            raise InvalidUsernameOrPasswordError(LogsConfig.INVALID_USERNAME_OR_PASSWORD)

        # Invalid password
        if player[0][1] != hashlib.sha256(password.encode()).hexdigest():
            logger.debug(LogsConfig.INVALID_USERNAME_OR_PASSWORD)
            logger.debug('Invalid password')
            raise InvalidUsernameOrPasswordError(LogsConfig.INVALID_USERNAME_OR_PASSWORD)
        rws = self.cur.execute(QueriesConfig.PLAYER_DATA, (player[0][0],))
        player_data = rws.fetchall()

        logged_in_player = Player(name=player[0][0], role=player[0][2], high_score=player_data[0][1], highscore_created_on=player_data[0][4], total_games_played=player_data[0][2], total_games_won=player_data[0][3])
        return logged_in_player

    def update_high_score(self, uname: str, new_high_score: float):
        self.cur.execute(QueriesConfig.UPDATE_HIGH_SCORE, (new_high_score, datetime.now(), uname))

    def get_leaderboard(self):
        rws = self.cur.execute(QueriesConfig.GET_LEADERBOARD)
        return [Leaderboard(uname=player_[0], high_score=player_[1], scored_on=player_[2]) for player_ in rws.fetchall()]

    def update_player_stats(self, total_games_played: int, total_games_won: int, uname: str):
        self.cur.execute(QueriesConfig.UPDATE_PLAYER_STATS, (total_games_played, total_games_won, uname))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_tb or exc_val:
            # re raises error on the callers side
            return False
        self.connection.commit()
        self.connection.close()
