import yaml
import os

path_current_directory = os.path.dirname(__file__)
HANGMAN_CONFIG_PATH = os.path.join(path_current_directory, 'hangman.yml')

class HangmanConfig:
    WELCOME_TO_GAME = None
    ALREADY_GUESSED = None
    CORRECT_GUESS = None
    ALL_GUESSED_CORRECTLY = None
    NOT_GUESSED_CORRECTLY = None
    YOUR_GUESS = None
    ENTER_SINGLE_CHARACTER = None
    RESULT_OF_SINGLE_ROUND = None
    ROUND_INFO = None
    HANGMAN_WORD = None
    HANGMAN_CHANCES = None
    HANGMAN_HINT = None

    @classmethod
    def load(cls):
        with open(HANGMAN_CONFIG_PATH, 'r') as f:
            data = yaml.safe_load(f)
            cls.WELCOME_TO_GAME = data['WELCOME_TO_GAME']
            cls.ALREADY_GUESSED = data['ALREADY_GUESSED']
            cls.CORRECT_GUESS = data['CORRECT_GUESS']
            cls.ALL_GUESSED_CORRECTLY = data['ALL_GUESSED_CORRECTLY']
            cls.NOT_GUESSED_CORRECTLY = data['NOT_GUESSED_CORRECTLY']
            cls.YOUR_GUESS = data['YOUR_GUESS']
            cls.ENTER_SINGLE_CHARACTER = data['ENTER_SINGLE_CHARACTER']
            cls.RESULT_OF_SINGLE_ROUND = data['RESULT_OF_SINGLE_ROUND']
            cls.ROUND_INFO = data['ROUND_INFO']
            cls.HANGMAN_WORD = data['HANGMAN_WORD']
            cls.HANGMAN_CHANCES = data['HANGMAN_CHANCES']
            cls.HANGMAN_HINT = data['HANGMAN_HINT']
