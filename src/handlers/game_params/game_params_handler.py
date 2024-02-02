from src.DBUtils.database import Database
from src.DBUtils.game_config.GameConfigDAO import GameConfigDAO
from src.config.api.api_config import ApiConfig
from src.handlers.base_handler.base_handler import BaseHandler


class GameParamsHandler(BaseHandler):
    def __init__(self, db: Database):
        super().__init__(db)

    def get_game_params(self):
        with GameConfigDAO(self.db.connection) as g_config_dao:
            round_options = g_config_dao.get_game_params(ApiConfig.GAME_PARAMS_ROUND)
            difficulty_options = g_config_dao.get_game_params(ApiConfig.GAME_PARAMS_DIFFICULTY)

        return {
            ApiConfig.GAME_PARAMS_ROUND: round_options,
            ApiConfig.GAME_PARAMS_DIFFICULTY: difficulty_options
        }
