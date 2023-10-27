import sqlite3
import logging
import hashlib
from datetime import datetime
from config.config import Config
from utils.exception import AlreadyExistsError
from utils.exception import InvalidUsernameOrPasswordError
from utils.named_tuples import Player,Leaderboard


CREATE_TABLE_AUTH = "CREATE TABLE IF NOT EXISTS auth_table (uname TEXT PRIMARY KEY, password TEXT, role TEXT)"
CREATE_TABLE_PLAYER = "CREATE TABLE IF NOT EXISTS players(uname TEXT PRIMARY KEY, high_score REAL, total_game INTEGER, total_games_won INTEGER, high_score_created_on timestamp, FOREIGN KEY (uname) REFERENCES auth_table(uname))"
FIND_USER_QUERY = "SELECT * FROM auth_table WHERE uname=?"
INSERT_INTO_AUTH = "INSERT INTO auth_table VALUES(?,?,?)"
INSERT_INTO_PLAYERS = "INSERT INTO players VALUES(?,0,0,0,?)"
PLAYER_DATA = "SELECT * FROM players WHERE uname=?"
UPDATE_HIGH_SCORE = "UPDATE players SET high_score = ?, high_score_created_on=?  WHERE uname = ?"
GET_LEADERBOARD = "SELECT uname, high_score,high_score_created_on from players ORDER BY high_score DESC,high_score_created_on DESC LIMIT 10"
UPDATE_PLAYER_STATS = "UPDATE players SET total_game = ?, total_games_won=? WHERE uname = ?"
ALREADY_EXIST_ERROR = "Username taken"
INVALID_USERNAME_OR_PASSWORD = "Invalid username or password"
logger = logging.getLogger("main.database")


class PlayerDAO:
    singleton = 1

    def __init__(self):
        self.connection = sqlite3.connect(Config.DBPATH)
        self.cur = self.connection.cursor()
        # Create table only once
        if self.singleton != 0:
            logger.info("Three tables are created")
            self.cur.execute(CREATE_TABLE_AUTH)
            self.cur.execute(CREATE_TABLE_PLAYER)
            self.connection.commit()
            self.singleton -= 1

    def find_user(self, uname: str):
        """ Finds a user in the database with given username """
        rws = self.cur.execute(FIND_USER_QUERY, (uname,))
        return rws

    def signup(self, uname: str, password: str):
        # Already exists
        if self.find_user(uname).rowcount != 0:
            logger.error(ALREADY_EXIST_ERROR)
            raise AlreadyExistsError(ALREADY_EXIST_ERROR)
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cur.execute(INSERT_INTO_AUTH, (uname, hashed_password, "player"))
        self.cur.execute(INSERT_INTO_PLAYERS, (uname, datetime.now()))

    def login(self, uname: str, password: str):
        rws = self.find_user(uname)
        player = rws.fetchall()
        # Invalid Username
        if len(player) == 0:
            logger.debug(INVALID_USERNAME_OR_PASSWORD)
            raise InvalidUsernameOrPasswordError(INVALID_USERNAME_OR_PASSWORD)

        # Invalid password
        if player[0][1] != hashlib.sha256(password.encode()).hexdigest():
            logger.debug(INVALID_USERNAME_OR_PASSWORD)
            # logging.debug(player)
            raise InvalidUsernameOrPasswordError(INVALID_USERNAME_OR_PASSWORD)
        rws = self.cur.execute(PLAYER_DATA, (player[0][0],))
        player_data = rws.fetchall()

        logged_in_player = Player(name=player[0][0], role=player[0][2], high_score=player_data[0][1], highscore_created_on=player_data[0][4], total_games_played=player_data[0][2], total_games_won=player_data[0][3])
        return logged_in_player

    def update_high_score(self, uname: str, new_high_score: float):
        self.cur.execute(UPDATE_HIGH_SCORE, (new_high_score, datetime.now(), uname))

    def get_leaderboard(self):
        rws = self.cur.execute(GET_LEADERBOARD)
        return [Leaderboard(uname=player_[0], high_score=player_[1], scored_on=player_[2]) for player_ in rws.fetchall()]

    def update_player_stats(self, total_games_played: int, total_games_won: int, uname: str):
        self.cur.execute(UPDATE_PLAYER_STATS, (total_games_played, total_games_won, uname))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_tb or exc_val:
            # re raises error on the callers side
            return False
        self.connection.commit()
        self.connection.close()

