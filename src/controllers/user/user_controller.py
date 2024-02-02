import logging

from fastapi import HTTPException
from starlette import status

from src.DBUtils.database.database import Database
from src.handlers.user.user_handler import UserHandler
from src.utils.exception import DatabaseException

logger = logging.getLogger('main.user_controller')


class UserController:
    @staticmethod
    def get_profile(user_id):
        try:
            db = Database()
            with UserHandler(db, user_id) as user_handler:
                user = user_handler.get_profile()
            return user

        except DatabaseException as db:
            logger.error(str(db))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(db))

