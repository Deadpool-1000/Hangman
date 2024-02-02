from src.DBUtils.database import Database
from src.handlers.game_params.game_params_handler import GameParamsHandler


class GameParamsController:
    @staticmethod
    def get_game_params():
        db = Database()
        with GameParamsHandler(db):
            pass

