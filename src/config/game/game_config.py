import yaml
GAME_CONFIGS_PATH = "src/config/game/game.yml"


class GameConfig:
    MAIN_MESSAGE = None
    SUCCESSFUL_SIGNUP = None
    WELCOME_TO_HANGMAN = None
    TRY_AGAIN = None
    SIGNUP_PROMPT = None
    LOGIN_PROMPT = None

    @classmethod
    def load(cls):
        with open(GAME_CONFIGS_PATH, 'r') as f:
            data = yaml.safe_load(f)
            cls.MAIN_MESSAGE = data['MAIN_MESSAGE']
            cls.SUCCESSFUL_SIGNUP = data['SUCCESSFUL_SIGNUP']
            cls.WELCOME_TO_HANGMAN = data['WELCOME_TO_HANGMAN']
            cls.TRY_AGAIN = data['TRY_AGAIN']
            cls.SIGNUP_PROMPT = data['SIGNUP_PROMPT']
            cls.LOGIN_PROMPT = data['LOGIN_PROMPT']
