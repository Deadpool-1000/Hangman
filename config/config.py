import yaml


class Config:
    """
    Maintains all the config variables of the game
    """
    MAIN_PROMPT = None
    ADMIN_PROMPT = None
    PLAYER_PROMPT = None
    MODIFY_GAME_PROMPT = None
    SECURE_PASSWORD_PROMPT = None

    @classmethod
    def load(cls):
        with open('config.yml', 'r') as f:
            data = yaml.safe_load(f)
            cls.MAIN_PROMPT = data['MAIN_PROMPT']
            cls.ADMIN_PROMPT = data['ADMIN_PROMPT']
            cls.PLAYER_PROMPT = data['PLAYER_PROMPT']
            cls.MODIFY_GAME_PROMPT = data['MODIFY_GAME_PROMPT']
            cls.SECURE_PASSWORD_PROMPT = data['SECURE_PASSWORD_PROMPT']
