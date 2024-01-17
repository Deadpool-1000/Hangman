import yaml
import os 

path_current_directory = os.path.dirname(__file__)
API_CONFIG_PATH = os.path.join(path_current_directory, 'api.yml')


class ApiConfig:
    ROLE_ADMIN = None
    ROLE_USER = None
    GAME_PARAMS_ROUND = None
    GAME_PARAMS_DIFFICULTY = None

    @classmethod
    def load(cls):
        with open(API_CONFIG_PATH, 'r') as f:
            data = yaml.safe_load(f)
            cls.ROLE_ADMIN = data['ROLE_ADMIN']
            cls.ROLE_USER = data['ROLE_USER']
            cls.GAME_PARAMS_ROUND = data['GAME_PARAMS_ROUND']
            cls.GAME_PARAMS_DIFFICULTY = data['GAME_PARAMS_DIFFICULTY']
