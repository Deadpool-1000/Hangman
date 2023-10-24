import logging
from player.user import User
from hangman.hangman import Hangman
from prompts.hangman_prompts import HangmanPrompts
from menu import menu
from os import system
logger = logging.getLogger('main.player')


class Player(User):
    """
        A class that represents player of the game
    """

    def __init__(self, name: str, role: str):
        super().__init__(name, role)
        logger.debug(f"Player {name} created")
        self.scores = []
        self.high_score = None
        self.total_wins = 0

    def __repr__(self) -> str:
        return f"<Player {self.name} Scores:{self.scores} Wins:{self.total_wins} />"

    def menu(self):
        user_operation = {
            'p': self.start_new_game,
            'l': self.display_leaderboard,
        }
        m = menu(HangmanPrompts.PLAYER_PROMPT, allowed=['p', 'l'])
        for game_choice in m:
            user_function = user_operation.get(game_choice)
            user_function()
            print("---------------------------------------------------")

    def start_new_game(self):
        hg = Hangman(self)
        hg.start_game()

    def display_leaderboard(self):
        pass

    def calculate_high_score(self):
        self.high_score = max(self.scores)
