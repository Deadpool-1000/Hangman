from fastapi import APIRouter, Depends

from src.DBUtils.game_config.GameConfigDAO import GameConfigDAO
from src.config.api.api_config import ApiConfig
from src.utils.rbac import get_token


game_params_router = APIRouter(tags=['Parameters'])


@game_params_router.get("/game_parameters", dependencies=[Depends(get_token)])
def get_game_params():
    with GameConfigDAO() as g_dao:
        round_options = g_dao.get_game_params(ApiConfig.GAME_PARAMS_ROUND)
        difficulty_options = g_dao.get_game_params(ApiConfig.GAME_PARAMS_DIFFICULTY)

        return {
            ApiConfig.GAME_PARAMS_ROUND: round_options,
            ApiConfig.GAME_PARAMS_DIFFICULTY: difficulty_options
        }
