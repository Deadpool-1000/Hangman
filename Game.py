import logging
from os import system
from player.admin import Admin
from player.player import Player
from hangman.graphic import hanged
from utils.exception import AlreadyExistsError, InvalidUsernameOrPasswordError
from db.PlayerDAO import PlayerDAO
from config.config import Config
from utils.utils import input_uname_and_password, validate_password, menu


logger = logging.getLogger('main.menu')
SUCCESSFUL_SIGNUP = "Successfully signed up 🎉\n"
WELCOME_TO_HANGMAN = "Welcome to Hangman"
TRY_AGAIN = "\nPlease try again"
SIGNUP_PROMPT = "For Signup, Please enter the following details: "
LOGIN_PROMPT = "For Login please enter the following details: "
ALREADY_EXIST_LOG = "Already exist error"
INVALID_UNAME_OR_PASSWORD_LOG = "Invalid username or password"


class Game:

    @classmethod
    def start_menu(cls) -> None:
        """
        Entry point for the application. Displays main menu of the game and calls appropriate function
        :return: None
        """
        game_functions = {
            'l': cls._login,
            's': cls._signup
        }
        m = menu(Config.MAIN_PROMPT, allowed=['l', 's'])
        for game_choice in m:
            game_function = game_functions.get(game_choice)
            system('cls')
            player: Admin | Player | None = game_function()
            if player is None:
                print(TRY_AGAIN)
                continue
            system('cls')
            print(WELCOME_TO_HANGMAN)
            print(hanged(6))
            player.menu()
            system('cls')

    @staticmethod
    def _login() -> Player | None:
        uname, password = input_uname_and_password(LOGIN_PROMPT)
        try:
            with PlayerDAO() as p_dao:
                player_tuple = p_dao.login(uname, password)
        except InvalidUsernameOrPasswordError:
            logger.error(INVALID_UNAME_OR_PASSWORD_LOG)
            return None

        logger.debug(f'{player_tuple}')

        if player_tuple.role == 'admin':
            return Admin(name=player_tuple.name, high_score=player_tuple.high_score,
                         highscore_created_on=player_tuple.highscore_created_on,
                         total_games_played=player_tuple.total_games_played,
                         total_games_won=player_tuple.total_games_won
            )
        else:
            new_player = Player(name=player_tuple.name, role='player',
                                high_score=player_tuple.high_score,
                                highscore_created_on=player_tuple.highscore_created_on,
                                total_games_played=player_tuple.total_games_played,
                                total_games_won=player_tuple.total_games_won
            )
            logger.info(f"Login with {new_player}")
            return new_player

    @classmethod
    def _signup(cls) -> Player | None:
        uname, password = input_uname_and_password(SIGNUP_PROMPT)
        password = validate_password(password)
        try:
            with PlayerDAO() as p_dao:
                p_dao.signup(uname=uname, password=password)
        except AlreadyExistsError as ae:
            logger.error(ALREADY_EXIST_LOG)
            print(ae)
            return None
        system('cls')
        print(SUCCESSFUL_SIGNUP)
        return cls._login()
