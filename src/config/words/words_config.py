import yaml
import os

path_current_directory = os.path.dirname(__file__)
WORDS_CONFIGS_PATH = os.path.join(path_current_directory, 'words.yml')


class WordsConfig:
    WORDS_FILE_PATH = None

    @classmethod
    def load(cls):
        with open(WORDS_CONFIGS_PATH, 'r') as f:
            data = yaml.safe_load(f)
            cls.WORDS_FILE_PATH = os.path.join(path_current_directory, f"../../{data['WORDS_FILE_PATH']}")
