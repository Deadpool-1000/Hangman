import yaml
import os

path_current_directory = os.path.dirname(__file__)
PROMPT_CONFIG_PATH = os.path.join(path_current_directory, 'prompt.yml')


class PromptConfig:
    """
    Maintains all the config variables of the game
    """
    DBPATH = None
    MAIN_PROMPT = None
    ADMIN_PROMPT = None
    PLAYER_PROMPT = None
    MODIFY_GAME_PROMPT = None
    INPUT_DIFFICULTY_PROMPT = None
    WORD_SECTION_PROMPT = None
    SECURE_PASSWORD_PROMPT = None

    @classmethod
    def load(cls):
        with open(PROMPT_CONFIG_PATH, 'r') as f:
            data = yaml.safe_load(f)
            cls.DBPATH = os.path.join(path_current_directory, f"../../{data['DBPATH']}")
            cls.MAIN_PROMPT = data['MAIN_PROMPT']
            cls.ADMIN_PROMPT = data['ADMIN_PROMPT']
            cls.PLAYER_PROMPT = data['PLAYER_PROMPT']
            cls.MODIFY_GAME_PROMPT = data['MODIFY_GAME_PROMPT']
            cls.SECURE_PASSWORD_PROMPT = data['SECURE_PASSWORD_PROMPT']
            cls.INPUT_DIFFICULTY_PROMPT = data['INPUT_DIFFICULTY_PROMPT']
            cls.WORD_SECTION_PROMPT = data['WORD_SECTION_PROMPT']
