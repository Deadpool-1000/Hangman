import logging
from player.player import Player
from menu import menu
from prompts.hangman_prompts import HangmanPrompts
from hangman.hangman import Hangman
from os import system
logger = logging.getLogger('main.admin')


class Admin(Player):
    """
        Admin class of the game.
        Has all the features the player has and can add or remove the words and get the list of existing users
    """
    def __init__(self, name) -> None:
        super().__init__(name, role="admin")
        logger.info("Admin logged in")

    def menu(self) -> None:
        admin_functionalities = {
            'l': self.display_leaderboard,
            'w': self.word_section,
            'p': self.game_section,
        }
        m = menu(prompt=HangmanPrompts.ADMIN_PROMPT, allowed=['l', 'w', 'p'])
        for admin_choice in m:
            admin_function = admin_functionalities.get(admin_choice)
            admin_function()

    @staticmethod
    def word_section():
        print("Word Section")
        pass

    def game_section(self):
        h = Hangman(self)
        h.start_game()

    @staticmethod
    def modify_game_settings():
        pass
