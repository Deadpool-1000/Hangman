from src.utils.utils import is_password_safe


class TestUtils:
    def test_is_password_safe_with_unsafe_password(self):
        return_val = is_password_safe('admin')
        assert return_val is False

    def test_is_password_safe_with_safe_password(self):
        return_val = is_password_safe('Admin@2002')
        assert return_val is True

    def test_input_game_params(self):
        pass

    def test_input_uname_and_password(self, monkeypatch):
        pass
