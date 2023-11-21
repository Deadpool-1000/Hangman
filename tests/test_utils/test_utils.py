import pytest
from datetime import datetime
from src.utils.utils import is_password_safe, get_good_input, format_date, menu


class TestUtils:
    def test_is_password_safe_with_empty(self):
        return_val = is_password_safe('')
        assert return_val is False

    def test_is_password_safe_with_unsafe_password(self):
        return_val = is_password_safe('admin')
        assert return_val is False

    def test_is_password_safe_with_safe_password(self):
        return_val = is_password_safe('Admin@2002')
        assert return_val is True

    def test_get_good_input_with_good_input(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: 'milind')
        assert get_good_input('', '') == 'milind'

    def test_good_input_with_empty_input(self, monkeypatch):
        my_inputs = iter(['', 'milind'])
        monkeypatch.setattr('builtins.input', lambda _: next(my_inputs))
        assert get_good_input('', '') == 'milind'

    @pytest.mark.parametrize("bad_dates", ['abc', '2023-10-15', 'lo', '  ', '2023-10-87 22:15:33.77777'])
    def test_format_date_with_bad_date(self, bad_dates):
        with pytest.raises(ValueError):
            format_date(bad_dates)

    @pytest.mark.parametrize('inp_date, expected', [('2023-10-25 11:37:54.637963', "25/10/2023 at 11:37")])
    def test_format_date_with_good_date(self, inp_date, expected):
        date: datetime = format_date(inp_date)
        assert date == expected

    @pytest.mark.parametrize('inp', [['a'], ['b', 'q']])
    def test_menu_with_valid_options(self, monkeypatch, inp):
        my_inputs = iter(inp)
        expected_val = iter(inp)
        monkeypatch.setattr('builtins.input', lambda _: next(my_inputs))
        m = menu('', ['a', 'b'])
        ret_val = next(m)
        assert ret_val == next(expected_val)

    @pytest.mark.parametrize('inp', [['', 'p', 'q'], ['p', 'p', 'q']])
    def test_menu_with_quit_option(self, monkeypatch, inp):
        my_inputs = iter(inp)
        monkeypatch.setattr('builtins.input', lambda _: next(my_inputs))
        with pytest.raises(StopIteration):
            m = menu('', ['q', 'a', 'b', 'c'])
            ret = next(m)
