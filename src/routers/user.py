from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.BLOCKLIST import BLOCKLIST
from src.controllers.user.signup_controller import SignupController
from src.controllers.user.user_controller import UserController
from src.schemas import UserSchema
from src.utils.jwt_helper import get_token
from src.controllers.user.login_controller import LoginController
from src.config import ApiConfig


# TODO why environment is not loading by using load_dotenv()

user_router = APIRouter(tags=['Authentication'])


@user_router.post('/signup', status_code=201)
def signup(user_data: UserSchema):
    message = SignupController.signup(user_data)
    return message


@user_router.post('/login', summary=ApiConfig.LOGIN_SUMMARY)
async def login(user_data: OAuth2PasswordRequestForm = Depends()):
    token = LoginController.login(user_data)
    return token


@user_router.post('/logout')
def logout(user=Depends(get_token)):
    jti = user['jti']
    BLOCKLIST.add(jti)
    print("Blocklist: ", BLOCKLIST)

    return {
        "message": ApiConfig.LOGOUT_SUCCESS_MESSAGE
    }


@user_router.get('/users/me', summary=ApiConfig.GET_PROFILE_SUMMARY)
def get_profile(token=Depends(get_token)):
    user_id = token['sub']
    user = UserController.get_profile(user_id)
    return user

