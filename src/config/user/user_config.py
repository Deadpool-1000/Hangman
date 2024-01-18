import yaml
import os

path_current_directory = os.path.dirname(__file__)
USER_CONFIG_PATH = os.path.join(path_current_directory, 'user.yml')


class UserConfig:
    ADMIN = None
    PLAYER = None

    @classmethod
    def load(cls):
        with open(USER_CONFIG_PATH, 'r') as f:
            data = yaml.safe_load(f)
            cls.ADMIN = data['ADMIN']
            cls.PLAYER = data['PLAYER']
