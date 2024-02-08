from fastapi import HTTPException
from starlette import status

from src.DBUtils import Database
from src.handlers import SignupHandler
from src.utils.exception import ApplicationError, DatabaseException


class SignupController:
    @staticmethod
    def signup(user_data):
        try:
            username = user_data.username
            password = user_data.password

            db = Database()
            with SignupHandler(db, username, password) as signup_handler:
                success = signup_handler.signup()
                if success:
                    return {
                        'message': 'Signup Successful.'
                    }

        except ApplicationError as ae:
            raise HTTPException(status_code=ae.code, detail=ae.message)

        except DatabaseException as db:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(db))
