from fastapi import APIRouter

from src.DBUtils.players.PlayerDAO import PlayerDAO
from src.schemas import LeaderboardSchema

leaderboard_router = APIRouter()


@leaderboard_router.get('/leaderboard')
def get_leaderboard():
    # with PlayerDAO() as p_dao:
    #     leader_board = p_dao.get_leaderboard()
    #     print(leader_board)
    #     return LeaderboardSchema(many=True).load(leader_board)
    return {
        "message": "Your Leaderboard."
    }
