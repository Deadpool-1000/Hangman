from fastapi import APIRouter, Depends
from starlette import status

from src.controllers import LeaderboardController
from src.utils.jwt_helper import get_token

leaderboard_router = APIRouter(tags=['Leaderboard'])


@leaderboard_router.get('/leaderboard', dependencies=[Depends(get_token)], status_code=status.HTTP_200_OK)
def get_leaderboard():
    leaderboard = LeaderboardController.get_leaderboard()
    return leaderboard
