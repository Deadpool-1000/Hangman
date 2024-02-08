from fastapi import APIRouter, Depends
from starlette import status

from src.controllers import GameParamsController
from src.utils.jwt_helper import get_token

game_params_router = APIRouter(tags=['Parameters'])


@game_params_router.get("/game-params", dependencies=[Depends(get_token)], status_code=status.HTTP_200_OK)
def get_game_params():
    game_params_data = GameParamsController.get_game_params()
    return game_params_data
