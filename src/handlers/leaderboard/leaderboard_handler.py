from src.DBUtils import PlayerDAO
from src.handlers import BaseHandler


class LeaderboardHandler(BaseHandler):
    def __init__(self, db):
        super().__init__(db)

    def get_leaderboard(self):
        with PlayerDAO(self.db.connection) as p_dao:
            leader_board = p_dao.get_leaderboard()
        return leader_board
