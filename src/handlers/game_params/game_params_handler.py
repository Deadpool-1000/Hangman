import logging
import sqlite3

from src.DBUtils import Database
from src.DBUtils import GameConfigDAO
from src.config import get_api_config
from src.handlers import BaseHandler
from src.utils.exception import DatabaseException

logger = logging.getLogger('main.game_params')

api_config = get_api_config()


class GameParamsHandler(BaseHandler):
    def __init__(self, db: Database):
        super().__init__(db)

    def get_game_params(self):
        try:
            with GameConfigDAO(self.db.connection) as g_config_dao:
                round_options = g_config_dao.get_game_params(api_config.GAME_PARAMS_ROUND)
                difficulty_options = g_config_dao.get_game_params(api_config.GAME_PARAMS_DIFFICULTY)

            return {
                api_config.GAME_PARAMS_ROUND: round_options,
                api_config.GAME_PARAMS_DIFFICULTY: difficulty_options
            }

        except sqlite3.Error as sql_error:
            logger.error(f'There was an error while getting game params {sql_error}')
            raise DatabaseException(
                'There was a problem while getting your game parameter data. Please try again later.')

    def is_difficulty_allowed(self, difficulty):
        with GameConfigDAO(self.db.connection) as g_config_dao:
            difficulty_parameters = g_config_dao.get_difficulty_options()
            difficulty_options = [difficulty_parameter[1] for difficulty_parameter in difficulty_parameters]

        return difficulty in difficulty_options
