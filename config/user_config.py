import yaml
USER_CONFIG_PATH = 'config_files/user.yml'


class UserConfig:
    PLAYER_REPR = None
    HIGH_SCORE_MESSAGE = None

    @classmethod
    def load(cls):
        with open(USER_CONFIG_PATH, 'r') as f:
            data = yaml.safe_load(f)
            cls.HIGH_SCORE_MESSAGE = data['HIGH_SCORE_MESSAGE']
            cls.PLAYER_REPR = data['PLAYER_REPR']