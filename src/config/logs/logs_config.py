import os

import yaml

path_current_directory = os.path.dirname(__file__)
LOG_CONFIG_PATH = os.path.join(path_current_directory, 'logs.yml')


class LogsConfig:
    ALREADY_EXIST_LOG = None
    INVALID_USERNAME_OR_PASSWORD = None
    OUT_OF_WORDS_ERROR_LOG = None
    PLAYER_RESULT_DEBUG = None

    @classmethod
    def load(cls):
        with open(LOG_CONFIG_PATH, 'r') as f:
            data = yaml.safe_load(f)
            cls.ALREADY_EXIST_LOG = data['ALREADY_EXIST_LOG']
            cls.INVALID_USERNAME_OR_PASSWORD = data['INVALID_USERNAME_OR_PASSWORD']
            cls.OUT_OF_WORDS_ERROR_LOG = data['OUT_OF_WORDS_ERROR_LOG']
            cls.PLAYER_RESULT_DEBUG = data['PLAYER_RESULT_DEBUG']
