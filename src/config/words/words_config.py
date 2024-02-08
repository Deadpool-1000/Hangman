import os
from functools import lru_cache

import yaml
from pydantic_settings import BaseSettings

data = dict()
path_current_directory = os.path.dirname(__file__)
WORDS_CONFIGS_PATH = os.path.join(path_current_directory, 'words.yml')
with open(WORDS_CONFIGS_PATH, 'r') as f:
    data.update(yaml.safe_load(f))


class WordsConfig(BaseSettings):
    WORDS_FILE_PATH: str = os.path.join(path_current_directory, f"../../{data['WORDS_FILE_PATH']}")


@lru_cache
def get_word_config():
    return WordsConfig()
