from fastapi import APIRouter, Depends

from src.DBUtils.players.PlayerDAO import PlayerDAO
from src.schemas import ScoreSchema
from src.utils.jwt_helper import get_token

score_router = APIRouter(tags=['Score'])


@score_router.put('/score', summary='Update score')
def update_score(score_data: ScoreSchema, token=Depends(get_token)):
    user_id = token['sub']
    with PlayerDAO() as p_dao:
        high_score = p_dao.get_high_score(user_id)

        # New High score
        if score_data["score"] > high_score:
            p_dao.update_high_score(user_id, score_data["score"])

        p_dao.update_player_stats(user_id=user_id, total_games_played=score_data["total_games_played"],
                                  total_games_won=score_data["total_games_won"])

    return {"message": "Score updated successfully"}
