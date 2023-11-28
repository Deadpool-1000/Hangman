import sqlite3

import pytest
from datetime import datetime
from src.utils.utils import is_password_safe, get_good_input, format_date, menu, input_uname_and_password, input_game_params, input_number_of_rounds, input_difficulty_level, get_available_round_options, get_available_difficulty_options, validate_password


class TestUtils:
    def test_is_password_safe_with_empty(self, my_config_loader):
        return_val = is_password_safe('')
        assert return_val is False

    def test_is_password_safe_with_unsafe_password(self, my_config_loader):
        return_val = is_password_safe('admin')
        assert return_val is False

    def test_is_password_safe_with_safe_password(self, my_config_loader):
        return_val = is_password_safe('Admin@2002')
        assert return_val is True

    def test_get_good_input_with_good_input(self, monkeypatch, my_config_loader):
        monkeypatch.setattr('builtins.input', lambda _: 'milind')
        assert get_good_input('', '') == 'milind'

    def test_good_input_with_empty_input(self, monkeypatch, my_config_loader):
        my_inputs = iter(['', 'milind'])
        monkeypatch.setattr('builtins.input', lambda _: next(my_inputs))
        assert get_good_input('', '') == 'milind'

    @pytest.mark.parametrize("bad_dates", ['abc', '2023-10-15', 'lo', '  ', '2023-10-87 22:15:33.77777'])
    def test_format_date_with_bad_date(self, bad_dates, my_config_loader):
        with pytest.raises(ValueError):
            format_date(bad_dates)

    @pytest.mark.parametrize('inp_date, expected', [('2023-10-25 11:37:54.637963', "25/10/2023 at 11:37")])
    def test_format_date_with_good_date(self, inp_date, expected, my_config_loader):
        date: datetime = format_date(inp_date)
        assert date == expected

    @pytest.mark.parametrize('inp', [['a', 'b'], ['b', 'a']])
    def test_menu_with_valid_options(self, monkeypatch, inp, my_config_loader):
        my_inputs = iter(inp)
        expected_val = iter(inp)
        monkeypatch.setattr('builtins.input', lambda _: next(my_inputs))
        m = menu('', ['a', 'b'])
        ret_val1 = next(m)
        ret_val2 = next(m)
        assert ret_val1 == next(expected_val) and ret_val2 == next(expected_val)

    @pytest.mark.parametrize('inp', [['', 'p', 'q'], ['p', 'p', 'q']])
    def test_menu_with_quit_option(self, monkeypatch, inp, my_config_loader):
        my_inputs = iter(inp)
        monkeypatch.setattr('builtins.input', lambda _: next(my_inputs))
        with pytest.raises(StopIteration):
            m = menu('', ['q', 'a', 'b', 'c'])
            next(m)

    def test_uname_password_with_empty(self, monkeypatch, my_config_loader):
        inps = iter(['test1', 'test2'])
        monkeypatch.setattr('src.utils.utils.get_good_input', lambda a, b: next(inps))
        uname, password = input_uname_and_password('Test Prompt')
        assert uname == 'test1' and password == 'test2'

    @pytest.mark.parametrize(('user_choice',), [(('5', '1'),), (('', '5', '6'), )])
    def test_input_game_params(self, monkeypatch, user_choice):
        user_choice_iter = iter(user_choice)
        monkeypatch.setattr('builtins.input', lambda _: next(user_choice_iter))
        ret_val = input_game_params('Test Prompt', params=(1, 3, 6))
        assert ret_val == int(user_choice[-1])

    def test_input_number_of_rounds(self, monkeypatch, my_config_loader):
        monkeypatch.setattr('src.utils.utils.get_available_round_options', lambda: [1, 3, 6])
        monkeypatch.setattr('src.utils.utils.input_game_params', lambda a, b: 1)
        ret_val = input_number_of_rounds()
        assert ret_val == 1

    @pytest.mark.parametrize(('user_choice', 'expected'), [(('e',), 7), (('m',), 8), (('p', 'd'), 12)])
    def test_input_difficult_level(self, monkeypatch, user_choice, expected, my_config_loader):
        user_choice_iter = iter(user_choice)
        monkeypatch.setattr('src.utils.utils.get_available_difficulty_options', lambda: [7, 8, 12])
        monkeypatch.setattr('builtins.input', lambda _: next(user_choice_iter))
        ret_val = input_difficulty_level()
        assert ret_val == expected

    def test_get_available_round_options(self, mocker, my_config_loader):
        mock_dao = mocker.MagicMock()
        mock_game_config_dao = mocker.MagicMock()
        mocker.patch('src.utils.utils.GameConfigDAO', mock_game_config_dao)
        mock_game_config_dao().__enter__.return_value = mock_dao
        mock_dao.get_round_options.return_value = [1, 3, 6]
        ret_val = get_available_round_options()
        assert ret_val == [1, 3, 6]

    def test_get_available_difficulty_options(self, mocker, my_config_loader):
        mock_dao = mocker.MagicMock()
        mock_game_config_dao = mocker.MagicMock()
        mocker.patch('src.utils.utils.GameConfigDAO', mock_game_config_dao)
        mock_game_config_dao().__enter__.return_value = mock_dao
        mock_dao.get_difficulty_options.return_value = [7, 8, 12]
        ret_val = get_available_difficulty_options()
        assert ret_val == [7, 8, 12]

    @pytest.mark.parametrize(('password', 'strong_password'), [(('Abcdef@2',), 'Abcdef@2'), (('qwerty', 'Abcdef@2'), 'Abcdef@2'),])
    def test_validate_password(self, monkeypatch, password, strong_password, my_config_loader):
        password = iter(password)
        monkeypatch.setattr('src.utils.utils.maskpass.advpass', lambda _: next(password))
        strong_password_ret_val = validate_password("abc")
        assert strong_password_ret_val == strong_password
