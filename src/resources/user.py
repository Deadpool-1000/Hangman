import sqlite3
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, get_jwt

from src.DBUtils.players.PlayerDAO import PlayerDAO
from src.utils.exception import InvalidUsernameOrPasswordError, AlreadyExistsError
from src.schemas import UserSchema, UserProfileSchema
from src.BLOCKLIST import BLOCKLIST


blp = Blueprint("Users", "users", description="Operation on users")


@blp.route('/signup')
class Signup(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        try:
            with PlayerDAO() as p_dao:
                p_dao.signup(**user_data)
            return {"message": "User Registered successfully."}
        except AlreadyExistsError:
            abort(409, message="Username taken.")
        except sqlite3.Error:
            abort(500, message="There was some problem. Try again later.")


@blp.route('/login')
class Login(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        try:
            with PlayerDAO() as p_dao:
                logged_in_player = p_dao.login(**user_data)
                token = create_access_token(identity=logged_in_player.id)
            return {"token": token}
        except InvalidUsernameOrPasswordError:
            abort(401, message="Invalid username or password")
        except sqlite3.Error:
            abort(500, message="There was some problem. Try again later.")


@blp.route('/logout')
class Logout(MethodView):
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']
        BLOCKLIST.add(jwt_id)
        return {
            "message": "Logout Successful."
        }


@blp.route('/user/me')
class User(MethodView):
    @jwt_required()
    @blp.doc(parameters=[
        {'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>',
         'required': 'true'}])
    @blp.response(200, UserProfileSchema)
    def get(self):
        user_id = get_jwt_identity()
        with PlayerDAO() as p_dao:
            user = p_dao.get_user_details(user_id)

        return UserProfileSchema().load({
            "id": user[0],
            "uname": user[1],
            "high_score": user[2],
            "total_game": user[3],
            "total_games_won": user[4],
            "high_score_created_on": user[5]
        })
