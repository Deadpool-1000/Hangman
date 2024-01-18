import re
import sqlite3

import maskpass
from datetime import datetime
from src.DBUtils.game_config.GameConfigDAO import GameConfigDAO
from src.config.prompts.prompts_config import PromptConfig
from src.config.utils.utils_config import UtilsConfig


def get_good_input(main_prompt: str, empty_prompt: str):
    user_input = input(main_prompt).strip()

    while len(user_input) == 0:
        user_input = input(empty_prompt).strip()

    return user_input



def menu(prompt: str, allowed: list[str]) -> str:
    """
    generator for menu that renders menu prompt repetitively and provides some basic input validation
    :yield str (user choice: a single character)
    """
    user_choice = input(prompt)
    while user_choice != 'q':
        if user_choice not in allowed:
            while user_choice not in allowed and user_choice != 'q':
                user_choice = input(UtilsConfig.VALID_INPUT)
            if user_choice == 'q':
                continue
        yield user_choice
        user_choice = input(prompt)


