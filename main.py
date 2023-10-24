import logging
import re
from player.admin import Admin
from player.player import Player
from prompts.hangman_prompts import HangmanPrompts
from menu import menu
from DB.PlayerDAO import PlayerDAO
from DB.PlayerDAO import AlreadyExistsError
from DB.PlayerDAO import InvalidUsernameOrPasswordError
from os import system
from hangman.graphic import hanged
# from rich import console

logging.basicConfig(format = "%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
                    datefmt = "%d-%M-%Y %H:%M:%S", level = logging.DEBUG, filename='logs.log')
logger = logging.getLogger("main")


# separate module for exception
class InvalidInput(Exception):
    pass


class BadInputError(Exception):
    pass


def login() -> Player | None:
    print("For login please enter the following details: ")
    uname = input("Username: ").strip()
    password = input("Password: ").strip()
    # uname, password = sanitize_input(uname, password)
    try:
        with PlayerDAO() as pd:
            player_tuple = pd.login(uname, password)
    except InvalidUsernameOrPasswordError:
        return None
    logger.debug(f'{player_tuple}')
    if player_tuple[1] == 'admin':
        return Admin(name=player_tuple[0])
    else:
        new_player = Player(name=player_tuple[0], role='player')
        logger.info(f"Login with {new_player}")
        return new_player


def signup() -> Player | None:
    print("Please enter the following details: ")
    uname = input("Username: ").strip()
    password = input("Password: ").strip()
    # uname, password = sanitize_input(uname, password)
    if not is_password_safe(password):
        print("Please choose a safe password: ")
        while not is_password_safe(password):
            password = input(HangmanPrompts.SECURE_PASSWORD_PROMPT)
    try:
        with PlayerDAO() as pd:
            pd.signup(uname=uname, password=password)
    except AlreadyExistsError as ae:
        print(ae)
        return None
    system('cls')
    print("Successfully signed up 🎉\n")
    return login()


game_functions = {
    'l': login,
    's': signup
}


def is_password_safe(password):
    """
    Your password must contain:
    1. Minimum eight characters,
    2. at least one uppercase letter
    3. one lowercase letter and one number
    :param password:
    :return: bool
    """
    rg = "^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$"
    if not re.match(rg, password):
        return False
    return True


def game_menu():
    m = menu(HangmanPrompts.MAIN_PROMPT, allowed=['l', 's'])
    for game_choice in m:
        game_function = game_functions.get(game_choice)
        system('cls')
        player: Admin | Player | None = game_function()
        if player is None:
            print("Please try again")
            continue
        system('cls')
        print("Welcome to Hangman ")
        print(hanged(6))
        player.menu()
        system('cls')


if __name__ == "__main__":
    with PlayerDAO() as pd:
        # pass
        pd.cur.execute('INSERT OR IGNORE INTO auth_table VALUES(?,?,?)', ("admin", "Abcde@2", "admin"))
        pd.cur.execute('INSERT OR IGNORE INTO players VALUES(?, 0, 0, 0)', ("admin",))
    game_menu()
