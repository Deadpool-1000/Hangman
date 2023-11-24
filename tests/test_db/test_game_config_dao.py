import pytest
import sqlite3
from src.db.game_config.GameConfigDAO import GameConfigDAO


sample_get_round_data = [
    (1, 'ROUND', 'OPTION1', 1),
    (2, 'ROUND', 'OPTION2', 3),
    (3, 'ROUND', 'OPTION3', 6),
]

sample_get_difficulty_data = [
    (4, 'LENGTH', 'EASY', 8),
    (5, 'LENGTH', 'MEDIUM', 10),
    (6, 'LENGTH', 'HARD', 12)

]


def mock_sqlite3_error():
    raise sqlite3.Error


@pytest.fixture
def mock_sqlite3_execute(mocker):
    mock_sqllite3 = mocker.patch('src.db.game_config.GameConfigDAO.sqlite3', spec=sqlite3)
    mock_execute = (
        mock_sqllite3
        .connect
        .return_value
        .cursor
        .return_value
        .execute
    )

    return mock_execute


class TestGameConfig:
    def test_get_game_params(self,  mock_sqlite3_execute):
        mock_sqlite3_execute.return_value.fetchall.return_value = sample_get_round_data
        with GameConfigDAO() as g_dao:
            data = g_dao.get_game_params('ROUND')
            assert data == [1, 3, 6]

    def test_get_round_options(self, mock_sqlite3_execute):
        mock_sqlite3_execute.return_value.fetchall.return_value = sample_get_round_data
        with GameConfigDAO() as g_dao:
            data = g_dao.get_round_options()
            assert data == [1, 3, 6]

    def test_get_difficulty_options(self, mock_sqlite3_execute):
        mock_sqlite3_execute.return_value.fetchall.return_value = sample_get_difficulty_data
        with GameConfigDAO() as g_dao:
            data = g_dao.get_difficulty_options()
            assert data == [8, 10, 12]

    def test_sqlite_error(self, mock_sqlite3_execute):
        mock_sqlite3_execute.return_value.fetchall = mock_sqlite3_error
        with pytest.raises(sqlite3.Error):
            with GameConfigDAO() as g_dao:
                data = g_dao.get_round_options()
