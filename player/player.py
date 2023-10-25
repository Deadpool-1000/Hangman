import logging
from player.user import User
from hangman.hangman import Hangman
from menu import menu
from typing import Callable
from DB.PlayerDAO import PlayerDAO
from config.config import Config

logger = logging.getLogger('main.player')


class Player(User):
    """
        A class that represents player of the game
    """

    def __init__(self, name: str, role: str, high_score: float):
        super().__init__(name, role)
        logger.debug(f"Player {name} created")
        self.scores: list[int] = []
        self.all_time_high_score: float = high_score
        self.total_wins: int = 0

    def __repr__(self) -> str:
        return f"<Player {self.name} Scores:{self.scores} Wins:{self.total_wins} />"

    def menu(self):
        user_operation: {str: Callable} = {
            'p': self.start_new_game,
            'l': self.display_leaderboard,
        }
        m = menu(prompt=Config.PLAYER_PROMPT, allowed=['p', 'l'])
        for game_choice in m:
            user_function = user_operation.get(game_choice)
            user_function()
            print("---------------------------------------------------")

    def start_new_game(self):
        hg = Hangman(self)
        hg.start_game()

    def display_leaderboard(self):
        pass

    @property
    def final_score(self) -> float:
        """
        Calculates the aggregate score of all games played by the player in one session.
        :return: float
        """
        current_score: float = sum(self.scores) / len(self.scores)
        if self._is_high_score(current_score):
            print("Congratulations you just made a high score")
            self.all_time_high_score = current_score
            self._update_high_score(self.all_time_high_score)
        return current_score

    def _is_high_score(self, current_score: float) -> bool:
        return True if self.all_time_high_score < current_score else False

    def _update_high_score(self, new_high_score: float) -> None:
        with PlayerDAO() as pd:
            pd.update_high_score(self.name, new_high_score)

