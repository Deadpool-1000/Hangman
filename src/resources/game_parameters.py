from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required

from src.DBUtils.game_config.GameConfigDAO import GameConfigDAO
from src.config.api.api_config import ApiConfig

blp = Blueprint("Game-Parameters", "game_parameters", description="Get Available Parameters for the game")


@blp.route("/game_parameters")
class GameParameters(MethodView):
    @jwt_required()
    @blp.doc(parameters=[
        {'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>',
         'required': 'true'}])
    def get(self):
        with GameConfigDAO() as g_dao:
            round_options = g_dao.get_game_params(ApiConfig.GAME_PARAMS_ROUND)
            difficulty_options = g_dao.get_game_params(ApiConfig.GAME_PARAMS_DIFFICULTY)

            return {
                ApiConfig.GAME_PARAMS_ROUND: round_options,
                ApiConfig.GAME_PARAMS_DIFFICULTY: difficulty_options
            }
