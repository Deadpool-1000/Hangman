from fastapi import APIRouter, Depends

from src.DBUtils.players.PlayerDAO import PlayerDAO
from src.utils.rbac import get_token

leaderboard_router = APIRouter(tags=['Leaderboard'])


@leaderboard_router.get('/leaderboard', dependencies=[Depends(get_token)])
def get_leaderboard():
    with PlayerDAO() as p_dao:
        leader_board = p_dao.get_leaderboard()
        return leader_board
