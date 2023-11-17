import logging
from os import system
from src.db.players.PlayerDAO import PlayerDAO
from src.utils.utils import format_date
from src.config.leaderboard.leaderboard_config import LeaderBoardConfig

logger = logging.getLogger("main.leaderboard")

NO_PLAYER_AVAILABLE_TO_SHOW = "No Players Available to show"
TOP_MESSAGE = "Here are the top scorers of the game"


class Leaderboard:
    def __init__(self):
        with PlayerDAO() as p_dao:
            self.leaderboard = p_dao.get_leaderboard()

    def show_leaderboard(self):
        system('cls')
        if len(self.leaderboard) == 0:
            print(LeaderBoardConfig.NO_PLAYER_AVAILABLE_TO_SHOW)
            return
        print(LeaderBoardConfig.TOP_MESSAGE)
        print("\n---------------------------------------------------")
        print(LeaderBoardConfig.TABLE_HEADER)
        try:
            for player_ in self.leaderboard:
                print(f'{player_.uname:20}{str(player_.high_score):20}{format_date(player_.scored_on):20}')
                print()
            print("---------------------------------------------------")
        except ValueError as err:
            print(err.args[0])
            return

