import pytest
from fastapi import HTTPException
from starlette import status

from src.controllers import SignupController
from src.utils.exception import ApplicationError, DatabaseException

SIGNUP_APPLICATION_ERROR_MESSAGE = "Username taken."
SIGNUP_DATABASE_ERROR_MESSAGE = "There was a problem signing you up."


def application_error():
    raise ApplicationError(code=status.HTTP_409_CONFLICT, message=SIGNUP_APPLICATION_ERROR_MESSAGE)


def database_exception():
    raise DatabaseException(SIGNUP_DATABASE_ERROR_MESSAGE)


@pytest.fixture
def mock_obj(mocker):
    return mocker.Mock()


@pytest.fixture
def mock_signup_handler(mocker):
    signup_handler = mocker.MagicMock()
    mock_signup_handler_obj = mocker.Mock()
    mocker.patch('src.controllers.user.signup_controller.SignupHandler', signup_handler)
    signup_handler().__enter__.return_value = mock_signup_handler_obj
    return mock_signup_handler_obj


@pytest.mark.order(1)
def test_signup_with_success(mock_obj, mock_signup_handler):
    mock_signup_handler.signup.return_value = True
    expected_return_value = {
        'message': 'Signup Successful.'
    }
    assert expected_return_value == SignupController.signup(mock_obj)


@pytest.mark.order(2)
def test_signup_with_application_error(mock_obj, mock_signup_handler):
    mock_signup_handler.signup = application_error
    with pytest.raises(HTTPException) as exc_info:
        SignupController.signup(mock_obj)
    assert exc_info.value.status_code == status.HTTP_409_CONFLICT


def test_signup_with_database_error(mock_obj, mock_signup_handler):
    mock_signup_handler.signup = database_exception
    with pytest.raises(HTTPException) as exc_info:
        SignupController.signup(mock_obj)
    assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

