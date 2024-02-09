import pytest
from fastapi import HTTPException
from starlette import status

from src.controllers import LeaderboardController
from src.utils.exception import DatabaseException

SAMPLE_LEADERBOARD = [
    {
        "uname": "admin",
        "high_score": 7.0,
        "high_score_created_on": "2024-02-04 22:47:25.154812"
    },
    {
        "uname": "my_deadpool",
        "high_score": 0.0,
        "high_score_created_on": "2024-02-02 13:20:28.237940"
    }
]

DATABASE_ERROR_MESSAGE = 'There was a problem fetching your leaderboard.'


def db_exc():
    raise DatabaseException(DATABASE_ERROR_MESSAGE)


@pytest.fixture
def mock_leaderboard_handler(mocker):
    leaderboard_handler_mock = mocker.MagicMock()
    leaderboard_handler_mock_obj = mocker.Mock()
    mocker.patch('src.controllers.leaderboard.leaderboard_controller.LeaderboardHandler', leaderboard_handler_mock)
    leaderboard_handler_mock().__enter__.return_value = leaderboard_handler_mock_obj
    return leaderboard_handler_mock_obj


def test_leaderboard_controller(mock_leaderboard_handler):
    mock_leaderboard_handler.get_leaderboard.return_value = SAMPLE_LEADERBOARD
    assert LeaderboardController.get_leaderboard() == SAMPLE_LEADERBOARD


def test_leaderboard_controller_with_db_exc(mock_leaderboard_handler):
    mock_leaderboard_handler.get_leaderboard = db_exc
    with pytest.raises(HTTPException) as exc:
        LeaderboardController.get_leaderboard()

    assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert exc.value.detail == DATABASE_ERROR_MESSAGE
