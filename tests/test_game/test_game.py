# import pytest
from src.utils.named_tuples import Player
from src.game.game import Game
from src.player.admin import Admin


class TestGame:
    def test_login_with_admin(self, mocker):
        m = mocker.MagicMock()
        mocker.patch('src.game.game.input_uname_and_password', lambda _: ('admin', 'admin'))
        mocker.patch('src.game.game.PlayerDAO', m)
        mocker.patch('src.game.game.PlayerDAO.login', lambda a, b: Player(name='admin', role='admin', high_score=7, highscore_created_on='2023-10-25 11:37:54.637963', total_games_played=5, total_games_won=3))
        ret_val = Game.login()
        assert isinstance(ret_val, Admin)
