import logging
logger = logging.getLogger("main.leaderboard")


class Leaderboard:
    def __init__(self, role):
        logger.info(f"{role} accessed the leaderboard section")
        self.role = role

    def modify_leaderboard(self):
        if self.role != 'a':
            return
        pass

    def show_leaderboard(self):
        pass