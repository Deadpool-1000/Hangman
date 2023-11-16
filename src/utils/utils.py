import re
import maskpass
from datetime import datetime
from src.db.game_config.GameConfigDAO import GameConfigDAO
from src.config.prompts.prompts_config import PromptConfig
from src.config.utils.utils_config import UtilsConfig


def format_date(date):
    date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    return f"{date.day}/{date.month}/{date.year} at {date.hour}:{date.minute}"


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


def input_uname_and_password(prompt: str) -> (str, str):
    print(prompt)
    uname = input(UtilsConfig.INPUT_USERNAME_PROMPT).strip()
    password = maskpass.advpass(UtilsConfig.INPUT_PASSWORD_PROMPT).strip()

    while len(uname) == 0:
        uname = input(UtilsConfig.EMPTY_UNAME_FOUND).strip()
    while len(password) == 0:
        password = input(UtilsConfig.EMPTY_PASSWORD_FOUND).strip()

    return uname, password


def is_password_safe(password):
    """
    Your password must contain:
    1. Minimum eight characters,
    2. at least one uppercase letter,
    3. one lowercase letter and one number
    :param password:
    :return: bool
    """
    rg = "^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$"
    if not re.match(rg, password):
        return False
    return True


def input_game_params(prompt: str, params: list[int]):
    print(prompt)
    print("\t|\t".join([str(round_) for round_ in params]))
    params = [str(num) for num in params]
    user_choice = input(UtilsConfig.YOUR_CHOICE)
    while user_choice not in params:
        user_choice = input(UtilsConfig.VALID_INPUT)
    return int(user_choice)


def input_number_of_rounds() -> int:
    round_options = get_available_round_options()
    return input_game_params(UtilsConfig.INPUT_ROUND_PROMPT, round_options)


def get_available_round_options() -> list[int]:
    with GameConfigDAO() as g_dao:
        round_options: list[int] = g_dao.get_round_options()
    return round_options


def validate_password(password):
    if not is_password_safe(password):
        print(PromptConfig.SECURE_PASSWORD_PROMPT)
        while not is_password_safe(password):
            password = maskpass.advpass(UtilsConfig.SAFE_PASSWORD_PROMPT)
    return password


def get_available_difficulty_options() -> list[int]:
    with GameConfigDAO() as g_dao:
        diff_options: list[int] = g_dao.get_difficulty_options()
    return diff_options


def input_difficulty_level():
    diff_options = get_available_difficulty_options()
    available = {
        'e': diff_options[0],
        'm': diff_options[1],
        'd': diff_options[2]
    }
    user_choice = input(PromptConfig.INPUT_DIFFICULTY_PROMPT)
    while user_choice not in available.keys():
        user_choice = input(UtilsConfig.VALID_INPUT)

    return available.get(user_choice)
