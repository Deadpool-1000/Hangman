import logging
from os import system
from db.PlayerDAO import PlayerDAO
from utils.utils import format_date
logger = logging.getLogger("main.leaderboard")


class Leaderboard:
    def __init__(self):
        with PlayerDAO() as p_dao:
            self.leaderboard = p_dao.get_leaderboard()

    def show_leaderboard(self):
        system('cls')
        if len(self.leaderboard) == 0:
            print("No Players Available to show")
            return
        print("Here are the top scorers of the game")
        print("\n---------------------------------------------------")
        print(f"{'Username':20}{'High Score':20}{'Scored On':20}")
        for player_ in self.leaderboard:
            print(f'{player_.uname:20}{str(player_.high_score):20}{format_date(player_.scored_on):20}')
            print()
        print("---------------------------------------------------")

