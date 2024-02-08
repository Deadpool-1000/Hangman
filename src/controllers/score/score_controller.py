from fastapi import HTTPException

from src.DBUtils import Database
from src.handlers import ScoreHandler
from src.utils.exception import DatabaseException


class ScoreController:
    @staticmethod
    def update_score(user_id, score_data):
        try:
            db = Database()
            with ScoreHandler(db, user_id, score_data) as score_handler:
                score_handler.update_player_score()
            return {
                'message': 'Score Updated Successfully.'
            }
        except DatabaseException as db:
            raise HTTPException(500, detail=str(db))
