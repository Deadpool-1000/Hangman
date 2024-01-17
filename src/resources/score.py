from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.DBUtils.players.PlayerDAO import PlayerDAO
from src.schemas import ScoreSchema


blp = Blueprint("Scores", "score", description="Operation on score")


@blp.route('/score')
class Score(MethodView):
    @jwt_required()
    @blp.doc(parameters=[
        {'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>',
         'required': 'true'}])
    @blp.arguments(ScoreSchema)
    def put(self, score_data):
        user_id = get_jwt_identity()
        with PlayerDAO() as p_dao:
            high_score = p_dao.get_high_score(user_id)
            if score_data["score"] > high_score:
                p_dao.update_high_score(user_id, score_data["score"])
            p_dao.update_player_stats(user_id=user_id, total_games_played=score_data["total_games_played"], total_games_won=score_data["total_games_won"])
        return {"message": "Score updated successfully"}, 200
