from player.player import Player
from utils.utils import menu
from typing import Callable
from config.prompt import PromptConfig
from word_section.words import WordMachine


class Admin(Player):
    """
        Admin of the game.
        Has all the features the player has and can add or remove the words and get the list of existing users
    """
    def __init__(self, name: str, high_score: float, total_games_played: int, total_games_won: int, highscore_created_on: str) -> None:
        super().__init__(
            name=name, role="admin",
            high_score=high_score,
            highscore_created_on=highscore_created_on,
            total_games_played=total_games_played,
            total_games_won=total_games_won
        )

    def menu(self) -> None:
        admin_functionalities: {str: Callable} = {
            'l': self.display_leaderboard,
            'w': self.word_section,
            'p': self.start_new_game,
            's': self.my_stats
        }
        m = menu(prompt=PromptConfig.ADMIN_PROMPT, allowed=['l', 'w', 'p', 's'])
        for admin_choice in m:
            admin_function = admin_functionalities.get(admin_choice)
            admin_function()

    @staticmethod
    def word_section():
        word_section = WordMachine()
        word_section.menu()
