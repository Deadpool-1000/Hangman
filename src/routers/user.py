import sqlite3


from fastapi import APIRouter, Body

from src.DBUtils.players.PlayerDAO import PlayerDAO
from src.utils.exception import InvalidUsernameOrPasswordError, AlreadyExistsError
from src.schemas import UserSchema, UserProfileSchema
from src.BLOCKLIST import BLOCKLIST


user_router = APIRouter(tags=['user', 'authentication'])


@user_router.post('/signup')
def signup(user_data: UserSchema):
    # try:
    #     with PlayerDAO() as p_dao:
    #         p_dao.signup(**user_data)
    #     return {"message": "User Registered successfully."}
    # except AlreadyExistsError:
    #     # abort(409, message="Username taken.")
    # except sqlite3.Error:
    #     # abort(500, message="There was some problem. Try again later.")
    return {
        "message": "Registration Successful."
    }


@user_router.post('/login')
def login(user_data: UserSchema):
    # try:
    #     with PlayerDAO() as p_dao:
    #         logged_in_player = p_dao.login(**user_data)
    #         token = create_access_token(identity=logged_in_player.id)
    #     return {"token": token}
    # except InvalidUsernameOrPasswordError:
    #     abort(401, message="Invalid username or password")
    # except sqlite3.Error:
    #     abort(500, message="There was some problem. Try again later.")
    return {
        "message": "Login successful."
    }


@user_router.post('/logout')
def logout():
    # jwt_id = get_jwt()['jti']
    # BLOCKLIST.add(jwt_id)
    return {
        "message": "Logout Successful."
    }


@user_router.get('/users/me')
def get_profile():
    # user_id = get_jwt_identity()
    # with PlayerDAO() as p_dao:
    #     user = p_dao.get_user_details(user_id)
    #
    # return UserProfileSchema().load({
    #     "id": user[0],
    #     "uname": user[1],
    #     "high_score": user[2],
    #     "total_game": user[3],
    #     "total_games_won": user[4],
    #     "high_score_created_on": user[5]
    # })
    return {
        "profile": {
            "name": "John Doe",
        }
    }
