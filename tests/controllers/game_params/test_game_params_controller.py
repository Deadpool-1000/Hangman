import pytest
from fastapi import HTTPException
from starlette import status

from src.controllers.game_params.game_params_controller import GameParamsController
from src.utils.exception import DatabaseException

SAMPLE_GAME_PARAMS = {
    "ROUND": (
        (
            "OPTION1",
            1
        ),
        (
            "OPTION2",
            3
        ),
        (
            "OPTION3",
            6
        )
    ),
    "DIFFICULTY": (
        (
            "EASY",
            8
        ),
        (
            "MEDIUM",
            10
        ),
        (
            "HARD",
            12
        )
    )
}

DATABASE_ERROR_MESSAGE = "There was a problem getting game params."


def db_exc():
    raise DatabaseException(DATABASE_ERROR_MESSAGE)


@pytest.fixture
def mock_game_params_handler(mocker):
    game_params_handler_mock = mocker.MagicMock()
    game_params_handler_mock_object = mocker.Mock()

    mocker.patch('src.controllers.game_params.game_params_controller.GameParamsHandler', game_params_handler_mock)
    game_params_handler_mock().__enter__.return_value = game_params_handler_mock_object

    return game_params_handler_mock_object


def test_game_params(mock_game_params_handler):
    mock_game_params_handler.get_game_params.return_value = SAMPLE_GAME_PARAMS
    assert GameParamsController.get_game_params() == SAMPLE_GAME_PARAMS


def test_game_params_with_db_exc(mock_game_params_handler):
    mock_game_params_handler.get_game_params = db_exc
    with pytest.raises(HTTPException) as exc:
        GameParamsController.get_game_params()

    assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert exc.value.detail == DATABASE_ERROR_MESSAGE
