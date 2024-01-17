from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from src.DBUtils.players.PlayerDAO import PlayerDAO
from src.schemas import LeaderboardSchema

blp = Blueprint("Leaderboard", "leaderboard", description="Get leaderboard of the game")


@blp.route('/leaderboard')
class LeaderBoard(MethodView):
    @jwt_required()
    @blp.doc(parameters=[
        {'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>',
         'required': 'true'}])
    @blp.response(200, LeaderboardSchema(many=True))
    def get(self):
        with PlayerDAO() as p_dao:
            leader_board = p_dao.get_leaderboard()
            print(leader_board)
            return LeaderboardSchema(many=True).load(leader_board)
