from fastapi import HTTPException

from src.DBUtils import Database
from src.handlers import LeaderboardHandler
from src.utils.exception import DatabaseException


class LeaderboardController:
    @staticmethod
    def get_leaderboard():
        try:
            db = Database()
            with LeaderboardHandler(db) as leaderboard_handler:
                leaderboard = leaderboard_handler.get_leaderboard()
                return leaderboard

        except DatabaseException as db:
            raise HTTPException(500, detail=str(db))
