from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.BLOCKLIST import BLOCKLIST
from src.config import get_api_config
from src.controllers import LoginController
from src.controllers import SignupController
from src.controllers import UserController
from src.schemas import UserSchema
from src.utils.jwt_helper import get_token

api_config = get_api_config()
user_router = APIRouter(tags=['Authentication'])


@user_router.post('/signup', status_code=status.HTTP_201_CREATED)
def signup(user_data: UserSchema):
    message = SignupController.signup(user_data)
    return message


@user_router.post('/login', summary=api_config.LOGIN_SUMMARY, status_code=status.HTTP_200_OK)
async def login(user_data: OAuth2PasswordRequestForm = Depends()):
    token = LoginController.login(user_data)
    return token


@user_router.post('/logout', status_code=status.HTTP_200_OK)
def logout(user=Depends(get_token)):
    jti = user['jti']
    BLOCKLIST.add(jti)
    print("Blocklist: ", BLOCKLIST)

    return {
        "message": api_config.LOGOUT_SUCCESS_MESSAGE
    }


@user_router.get('/users/me', summary=api_config.GET_PROFILE_SUMMARY, status_code=status.HTTP_200_OK)
def get_profile(token=Depends(get_token)):
    user_id = token['sub']
    user = UserController.get_profile(user_id)
    return user
