import logging
import sqlite3

from src.DBUtils import Database
from src.DBUtils import GameParamsDAO
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
            with GameParamsDAO(self.db.connection) as game_params_dao:
                round_options = game_params_dao.get_game_params(api_config.GAME_PARAMS_ROUND)
                difficulty_options = game_params_dao.get_game_params(api_config.GAME_PARAMS_DIFFICULTY)

            return {
                api_config.GAME_PARAMS_ROUND: round_options,
                api_config.GAME_PARAMS_DIFFICULTY: difficulty_options
            }

        except sqlite3.Error:
            logger.error(f'There was an error while getting game params')
            raise DatabaseException(
                'There was a problem while getting your game parameter data. Please try again later.')

    def is_difficulty_allowed(self, difficulty):
        with GameParamsDAO(self.db.connection) as g_params_dao:
            difficulty_parameters = g_params_dao.get_difficulty_options()
            difficulty_options = [difficulty_parameter[1] for difficulty_parameter in difficulty_parameters]

        return difficulty in difficulty_options

    def change_game_params(self, new_game_params):
        with GameParamsDAO(self.db.connection) as g_params_dao:
            formatted_new_game_params = self.format_game_params(new_game_params)
            g_params_dao.update_game_params(formatted_new_game_params)

    @staticmethod
    def format_game_params(game_params):
        round_params = game_params['ROUND']
        difficulty_params = game_params['DIFFICULTY']
        formatted_game_params = []
        for round_option in round_params:
            round_data = (round_option[1], round_option[0])
            formatted_game_params.append(round_data)

        for difficulty_option in difficulty_params:
            difficulty_data = (difficulty_option[1], difficulty_option[0])
            formatted_game_params.append(difficulty_data)

        return formatted_game_params

