import pytest
from fastapi import HTTPException
from starlette import status

from src.controllers import ScoreController
from src.utils.exception import DatabaseException


@pytest.fixture
def mock_score_handler(mocker):
    score_handler_mock = mocker.MagicMock()
    score_handler_mock_obj = mocker.Mock()

    mocker.patch('src.controllers.score.score_controller.ScoreHandler', score_handler_mock)
    score_handler_mock().__enter__.return_value = score_handler_mock_obj

    return score_handler_mock_obj


# Test data
DATABASE_ERROR_MESSAGE = "There was a problem updating your score"
TEST_USER_ID = '1sef4'
TEST_SCORE_DATA = {
    "score": 7,
    "total_games_played": 1,
    "total_games_won": 1
}
SUCCESS_MESSAGE = {
        'message': 'Score Updated Successfully.'
}


def db_exc():
    raise DatabaseException(DATABASE_ERROR_MESSAGE)


def test_score_controller(mocker, mock_score_handler):
    mock_score_handler.update_player_score = lambda: ...

    success_message = ScoreController.update_score(TEST_USER_ID, TEST_SCORE_DATA)
    assert success_message == SUCCESS_MESSAGE


def test_score_controller_with_db_exc(mock_score_handler):
    mock_score_handler.update_player_score = db_exc
    with pytest.raises(HTTPException) as exc:
        ScoreController.update_score(TEST_USER_ID, TEST_SCORE_DATA)

    assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert exc.value.detail == DATABASE_ERROR_MESSAGE
