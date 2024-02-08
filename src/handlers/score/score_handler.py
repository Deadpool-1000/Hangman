import logging
import sqlite3

from src.DBUtils import Database, PlayerDAO
from src.handlers import BaseHandler
from src.utils.exception import DatabaseException

logger = logging.getLogger('main.score_handler')


class ScoreHandler(BaseHandler):
    def __init__(self, db: Database, user_id, score_data):
        super().__init__(db)
        self.user_id = user_id
        self.score_data = score_data

    def update_player_score(self):
        try:
            with PlayerDAO(self.db.connection) as p_dao:
                high_score = p_dao.get_high_score(self.user_id)

                # New High score
                if self.score_data["score"] > high_score:
                    p_dao.update_high_score(self.user_id, self.score_data["score"])

                p_dao.update_player_stats(user_id=self.user_id,
                                          total_games_played=self.score_data["total_games_played"],
                                          total_games_won=self.score_data["total_games_won"])

        except sqlite3.Error as sql_error:
            logger.error(f'There was an error while updating the score {sql_error}')
            raise DatabaseException('There was a problem updating the score. Please try again later.')
