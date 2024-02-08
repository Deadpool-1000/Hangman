from fastapi import HTTPException

from src.DBUtils import Database
from src.handlers import GameParamsHandler
from src.utils.exception import DatabaseException


class GameParamsController:
    @staticmethod
    def get_game_params():
        try:
            db = Database()
            with GameParamsHandler(db) as game_params_handler:
                game_params = game_params_handler.get_game_params()
            return game_params
        except DatabaseException as db:
            raise HTTPException(500, str(db))
