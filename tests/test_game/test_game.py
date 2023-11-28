import sqlite3

import pytest

from src.player.player import Player
from src.player.admin import Admin
from src.game.game import Game
from src.utils.exception import InvalidUsernameOrPasswordError, AlreadyExistsError
from src.utils.named_tuples import Player as PTuple


def mock_raise_invalid_uname_or_password(a, b):
    raise InvalidUsernameOrPasswordError()


def mock_raise_sqlite3_error(uname, password):
    raise sqlite3.Error


def mock_raise_sqlite3_prog_error(uname, password):
    raise sqlite3.ProgrammingError


def mock_raise_already_exists(uname, password):
    raise AlreadyExistsError


class TestGame:
    def test_login_with_player(self, mocker, my_config_loader):
        m = mocker.MagicMock()
        mocker.patch('src.game.game.PlayerDAO', m)
        m().__enter__().login = lambda a, b: PTuple(name='test', role='player', high_score=7.0, total_games_played=3, total_games_won=2, highscore_created_on='22222')
        mocker.patch('src.game.game.input_uname_and_password', lambda _: ('abc', 'bcd'))
        assert isinstance(Game.login(), Player)

    def test_login_with_admin(self, mocker):
        mocker.patch('src.game.game.input_uname_and_password', lambda _: ('abc', 'bcd'))
        m = mocker.MagicMock()
        mocker.patch('src.game.game.PlayerDAO', m)
        m().__enter__().login.return_value = PTuple(name='test', role='admin', high_score=7.0, total_games_played=3, total_games_won=2, highscore_created_on='22222')
        assert isinstance(Game.login(), Admin)

    def test_wrong_uname_or_password(self, mocker):
        mocker.patch('src.game.game.input_uname_and_password', lambda _: ('abc', 'bcd'))
        m = mocker.MagicMock()
        mocker.patch('src.game.game.PlayerDAO', m)
        m().__enter__().login = mock_raise_invalid_uname_or_password
        assert Game.login() is None

    def test_sqlite_error(self, mocker):
        mocker.patch('src.game.game.input_uname_and_password', lambda _: ('abc', 'bcd'))
        m = mocker.MagicMock()
        mocker.patch('src.game.game.PlayerDAO', m)
        m().__enter__().login = mock_raise_sqlite3_error
        assert Game.login() is None

    def test_sqlite_prog_error(self, mocker):
        mocker.patch('src.game.game.input_uname_and_password', lambda _: ('abc', 'bcd'))
        m = mocker.MagicMock()
        mocker.patch('src.game.game.PlayerDAO', m)
        m().__enter__().login = mock_raise_sqlite3_prog_error
        assert Game.login() is None

    def test_signup_already_exists(self, mocker):
        mocker.patch('src.game.game.input_uname_and_password', lambda _: ('abc', 'bcd'))
        mocker.patch('src.game.game.validate_password', lambda _: _)
        mocker.patch('src.game.game.input_uname_and_password', lambda _: ('abc', 'bcd'))
        m = mocker.MagicMock()
        mocker.patch('src.game.game.PlayerDAO', m)
        m().__enter__().signup = mock_raise_already_exists
        ret_val = Game.signup()
        assert ret_val is None

    def test_signup_sqlite3_error(self, mocker):
        mocker.patch('src.game.game.input_uname_and_password', lambda _: ('abc', 'bcd'))
        mocker.patch('src.game.game.validate_password', lambda _: _)
        mocker.patch('src.game.game.input_uname_and_password', lambda _: ('abc', 'bcd'))
        m = mocker.MagicMock()
        mocker.patch('src.game.game.PlayerDAO', m)
        m().__enter__().signup = mock_raise_sqlite3_error
        ret_val = Game.signup()
        assert ret_val is None

    def test_success_signup(self, mocker):
        mock_login = mocker.Mock()
        mocker.patch('src.game.game.input_uname_and_password', lambda _: ('abc', 'bcd'))
        mocker.patch('src.game.game.validate_password', lambda _: _)
        mocker.patch('src.game.game.input_uname_and_password', lambda _: ('abc', 'bcd'))
        mocker.patch.object(Game, 'login', mock_login)
        m = mocker.MagicMock()
        mocker.patch('src.game.game.PlayerDAO', m)
        m().__enter__().signup = lambda uname, password: None
        Game.signup()
        mock_login.assert_called_once()
