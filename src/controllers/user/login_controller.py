from datetime import timedelta
from fastapi import HTTPException
from starlette import status

from src.DBUtils.database import Database
from src.config import get_api_config
from src.handlers import LoginHandler
from src.utils.exception import DatabaseException, ApplicationError
from src.utils.jwt_helper import create_access_token

api_config = get_api_config()


class LoginController:
    @staticmethod
    def login(user_data):
        try:
            # It is an oauth-form not a dictionary
            username = user_data.username
            password = user_data.password
            db = Database()

            with LoginHandler(db, username, password) as login_handler:
                user_auth_data = login_handler.login()
                payload = {
                    'sub': user_auth_data['user_id'],
                    'role': api_config.ADMIN if user_auth_data['role'] == 'admin' else api_config.PLAYER
                }
                token = create_access_token(payload, expires_delta=timedelta(minutes=20))

                return {
                    'access_token': token
                }

        except DatabaseException as db_exc:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(db_exc))

        except ApplicationError as ae:
            raise HTTPException(status_code=ae.code, detail=ae.message)
