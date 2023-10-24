import sqlite3
import logging
from collections import namedtuple
logger = logging.getLogger("main.database")


class AlreadyExistsError(Exception):
    pass


class InvalidUsernameOrPasswordError(Exception):
    pass


class PlayerDAO:
    singleton = 1

    def __init__(self):
        """Initialize db class variables"""
        self.connection = sqlite3.connect('./players.db')
        self.cur = self.connection.cursor()
        if self.singleton != 0:
            logger.info("Three tables are created")
            self.cur.execute("CREATE TABLE IF NOT EXISTS auth_table (uname TEXT PRIMARY KEY, password TEXT, role TEXT)")
            self.cur.execute("CREATE TABLE IF NOT EXISTS players(uname TEXT PRIMARY KEY, highscores INTEGER, total_game INTEGER, total_games_won INTEGER, FOREIGN KEY (uname) REFERENCES auth_table(uname))")
            self.cur.execute("CREATE TABLE IF NOT EXISTS game_config(config_id INTEGER PRIMARY KEY AUTOINCREMENT, config_name TEXT, config_key TEXT, config_value INTEGER)")
            self.connection.commit()
            self.singleton -= 1

    def find(self, uname):
        check_query = "SELECT * FROM auth_table WHERE uname=?"
        rws = self.cur.execute(check_query, (uname,))
        return rws

    def signup(self, uname, password):
        # Already exists
        if self.find(uname).rowcount == 0:
            raise AlreadyExistsError("A player with same username exists")
        query = "INSERT INTO auth_table VALUES(?,?,?)"
        player_query = "INSERT INTO players VALUES(?,0,0,0)"
        self.cur.execute(query, (uname, password, "player"))
        self.cur.execute(player_query, (uname,))
        self.connection.commit()

    def login(self, uname, password):
        rws = self.find(uname)
        player = rws.fetchall()
        # Invalid Username
        if len(player) == 0:
            logger.debug("Invalid username or password")
            raise InvalidUsernameOrPasswordError("Invalid Username or password")

        # Invalid password
        if player[0][1] != password:
            logger.debug("Invalid username or password2")
            logging.debug(player)
            raise InvalidUsernameOrPasswordError("Invalid Username or password")
        Player = namedtuple("Player", ('name', 'role'))
        logged_in_player = Player(name=player[0][0], role=player[0][2])
        return logged_in_player

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_tb or exc_val:
            # re raises error on the callers side
            return False
        self.connection.commit()
        self.connection.close()

