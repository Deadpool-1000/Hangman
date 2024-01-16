import sqlite3
import logging
from os import system
from src.user.admin import Admin
from src.user.player import Player
from src.hangman.graphic import hanged
from src.utils.exception import AlreadyExistsError, InvalidUsernameOrPasswordError
from src.DBUtils.players.PlayerDAO import PlayerDAO
from src.utils.utils import input_uname_and_password, validate_password, menu
from src.config.prompts.prompts_config import PromptConfig
from src.config.game.game_config import GameConfig

logger = logging.getLogger('main.mygame')


class Game:

    @classmethod
    def start_menu(cls) -> None:
        """
        Entry point for the application. Displays main menu of the game and calls appropriate function
        :return: None
        """
        game_functions = {
            'l': cls.login,
            's': cls.signup
        }
        print(GameConfig.MAIN_MESSAGE)
        m = menu(PromptConfig.MAIN_PROMPT, allowed=['l', 's'])
        for game_choice in m:
            game_function = game_functions.get(game_choice)
            system('cls')
            player: Admin | Player | None = game_function()
            if player is None:
                print(GameConfig.TRY_AGAIN)
                continue
            system('cls')
            print(GameConfig.WELCOME_TO_HANGMAN)
            print(hanged(6))
            player.menu()
            system('cls')

    @staticmethod
    def login() -> Player | None:
        uname, password = input_uname_and_password(GameConfig.LOGIN_PROMPT)
        try:
            with PlayerDAO() as p_dao:
                player_tuple = p_dao.login(uname, password)
        except InvalidUsernameOrPasswordError as e:
            system('cls')
            print(e)
            return None
        except sqlite3.ProgrammingError as err:
            logger.error(f'Database Programming error {err}')
            print('There was some problem 😔')
            return None
        except sqlite3.Error as err:
            logger.error(f'Database error {err}')
            print('There was some problem 😔')
            return None

        if player_tuple.role == 'admin':
            return Admin(
                user_id=player_tuple.id,
                name=player_tuple.name, high_score=player_tuple.high_score,
                highscore_created_on=player_tuple.highscore_created_on,
                total_games_played=player_tuple.total_games_played,
                total_games_won=player_tuple.total_games_won
            )
        else:
            new_player = Player(
                user_id=player_tuple.id,
                name=player_tuple.name, role='player',
                high_score=player_tuple.high_score,
                highscore_created_on=player_tuple.highscore_created_on,
                total_games_played=player_tuple.total_games_played,
                total_games_won=player_tuple.total_games_won
            )
            return new_player

    @classmethod
    def signup(cls) -> Player | None:
        uname, password = input_uname_and_password(GameConfig.SIGNUP_PROMPT)
        password = validate_password(password)
        try:
            with PlayerDAO() as p_dao:
                p_dao.signup(uname=uname, password=password)
        except AlreadyExistsError as ae:
            system('cls')
            print(ae)
            return None
        except sqlite3.Error as err:
            logger.error(err)
            print('There was some problem, please try again')
            return None
        system('cls')
        print(GameConfig.SUCCESSFUL_SIGNUP)
        return cls.login()
