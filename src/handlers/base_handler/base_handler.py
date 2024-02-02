from src.DBUtils.database import Database


class BaseHandler:
    def __init__(self, db: Database):
        self.db = db

    def __enter__(self):
        self.db.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_tb or exc_val:
            return False
        self.db.close()
