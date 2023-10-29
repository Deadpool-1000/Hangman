from os import system
from typing import Callable
from player.user import User
from hangman.hangman import Hangman
from db.PlayerDAO import PlayerDAO
from config.prompt import PromptConfig
from config.user_config import UserConfig
from utils.utils import menu, format_date, input_number_of_rounds, input_difficulty_level
from leaderboard.leaderboard import Leaderboard


class Player(User):
    """
        A class that represents player of the game
    """

    def __init__(self, name: str, role: str, high_score: float, total_games_played: int, total_games_won: int, highscore_created_on: str):
        super().__init__(name, role)
        self.scores: list[int] = []
        self.all_time_high_score: float = high_score
        self.total_wins: int = 0
        self.total_games_won = total_games_won
        self.total_games_played = total_games_played
        self.highscore_created_on = highscore_created_on

    def __repr__(self) -> str:
        return UserConfig.PLAYER_REPR.format(self.name, self.scores, self.total_wins)

    def menu(self):
        user_operation: {str: Callable} = {
            'p': self.start_new_game,
            'l': self.display_leaderboard,
            's': self.my_stats
        }
        m = menu(prompt=PromptConfig.PLAYER_PROMPT, allowed=['p', 'l', 's'])
        for game_choice in m:
            user_function = user_operation.get(game_choice)
            user_function()
            print("---------------------------------------------------")

    def start_new_game(self):
        system('cls')
        num_of_rounds = input_number_of_rounds()
        difficulty = input_difficulty_level()
        hg = Hangman(player=self, num_of_rounds=num_of_rounds, difficulty=difficulty)
        hg.start_game()

    @staticmethod
    def display_leaderboard():
        leader_board = Leaderboard()
        leader_board.show_leaderboard()

    @property
    def final_score(self) -> float:
        """
        Calculates the aggregate score of all games played by the player in one session.
        :return: float
        """
        current_score: float = sum(self.scores) / len(self.scores)
        if self._is_high_score(current_score):
            print(UserConfig.HIGH_SCORE_MESSAGE)
            self.all_time_high_score = current_score
            self._update_high_score(self.all_time_high_score)
        return current_score

    def _is_high_score(self, current_score: float) -> bool:
        return True if self.all_time_high_score < current_score else False

    def _update_high_score(self, new_high_score: float) -> None:
        with PlayerDAO() as pd:
            pd.update_high_score(self.name, new_high_score)

    def my_stats(self):
        system('cls')
        print(f"-------------------------{self.name}-------------------------")
        print("Total Games played: ", self.total_games_played)
        print("Total Games won: ", self.total_games_won)
        print(f'Your HighScore: {self.all_time_high_score} Created on: {format_date(self.highscore_created_on)}')
        print(f'-------------------------{"-"*len(self.name)}-------------------------')

    def update_stats(self, rounds_played, rounds_won):
        self.total_games_won += rounds_won
        self.total_games_played += rounds_played
        with PlayerDAO() as p_dao:
            p_dao.update_player_stats(self.total_games_played, self.total_games_won, self.name)

    def calculate_rounds_won(self):
        return len([i for i in self.scores if i > 0])
