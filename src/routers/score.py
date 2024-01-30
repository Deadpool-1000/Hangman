from fastapi import APIRouter

from src.DBUtils.players.PlayerDAO import PlayerDAO
from src.schemas import ScoreSchema

score_router = APIRouter(tags=['Score'])


@score_router.put('/score', summary='Update score')
def update_score(score_data: ScoreSchema):
    # user_id = get_jwt_identity()
    # with PlayerDAO() as p_dao:
    #     high_score = p_dao.get_high_score(user_id)
    #     if score_data["score"] > high_score:
    #         p_dao.update_high_score(user_id, score_data["score"])
    #     p_dao.update_player_stats(user_id=user_id, total_games_played=score_data["total_games_played"], total_games_won=score_data["total_games_won"])
    # return {"message": "Score updated successfully"}, 200
    return {
        "message": "Score updated Successfully."
    }
