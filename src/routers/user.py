import sqlite3
from dotenv import load_dotenv
from datetime import timedelta
from starlette import status
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.DBUtils.players.PlayerDAO import PlayerDAO
from src.utils.exception import InvalidUsernameOrPasswordError, AlreadyExistsError
from src.schemas import UserSchema
from src.BLOCKLIST import BLOCKLIST
from src.utils.utils import create_access_token
from src.utils.rbac import get_token


JWT_SECRET = "fIqrMcrIKjZqsEZdfwne82n8YsL6F3K0"
JWT_ALGO = "HS256"


# TODO why environment is not loading by using load_dotenv()

user_router = APIRouter(tags=['Authentication'])

LOGIN_SUMMARY = 'Create access token for user'
INVALID_USERNAME_OR_PASSWORD_MESSAGE = 'Invalid username or password'
DATABASE_ERROR_MESSAGE = 'There was some problem. Try again later.'
ADMIN = 'superman'
PLAYER = 'BATMAN'
GET_PROFILE_SUMMARY = 'Get your profile.'
SIGNUP_SUCCESS_MESSAGE = 'User Registered successfully.'
USERNAME_TAKEN_MESSAGE = 'Username taken.'
APPLICATION_ERROR_MESSAGE = 'There was some problem. Try again later.'
LOGOUT_SUCCESS_MESSAGE = 'Logout Successful.'


@user_router.post('/signup')
def signup(user_data: UserSchema):
    try:
        with PlayerDAO() as p_dao:
            p_dao.signup(**user_data.model_dump())
        return {
            "message": SIGNUP_SUCCESS_MESSAGE
        }
    except AlreadyExistsError:
        raise HTTPException(409, detail=USERNAME_TAKEN_MESSAGE)
    except sqlite3.Error:
        raise HTTPException(500, detail=APPLICATION_ERROR_MESSAGE)


@user_router.post('/login', summary=LOGIN_SUMMARY)
async def login(user_data: OAuth2PasswordRequestForm = Depends()):
    try:
        with PlayerDAO() as p_dao:
            logged_in_player = p_dao.login(user_data.username, user_data.password)
            payload = {
                'sub': logged_in_player['user_id'],
                'role': ADMIN if logged_in_player['role'] == 'admin' else PLAYER
            }
            token = create_access_token(payload, timedelta(minutes=20))
        return {"access_token": token}

    except InvalidUsernameOrPasswordError:
        raise HTTPException(401, detail=INVALID_USERNAME_OR_PASSWORD_MESSAGE)

    except sqlite3.Error:
        raise HTTPException(500, detail=DATABASE_ERROR_MESSAGE)


@user_router.post('/logout')
def logout(user=Depends(get_token)):
    jti = user['jti']
    BLOCKLIST.add(jti)
    print("Blocklist: ", BLOCKLIST)

    return {
        "message": LOGOUT_SUCCESS_MESSAGE
    }


@user_router.get('/users/me', summary=GET_PROFILE_SUMMARY)
def get_profile(user=Depends(get_token)):
    try:
        with PlayerDAO() as p_dao:
            user = p_dao.get_user_details(user['sub'])
        return user

    except Exception as e:
        print(e)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=APPLICATION_ERROR_MESSAGE
        )
