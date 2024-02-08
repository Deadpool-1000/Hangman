import pytest
from fastapi import HTTPException
from starlette import status

from src.controllers.user.login_controller import LoginController
from src.utils.exception import ApplicationError, DatabaseException

SAMPLE_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
LOGIN_DATABASE_ERROR_MESSAGE = 'There was some problem logging you in.'
LOGIN_APPLICATION_ERROR_MESSAGE = 'Invalid Username or password'


@pytest.fixture
def mock_login_handler(mocker):
    login_handler = mocker.MagicMock()
    mock_login_handler_object = mocker.Mock()
    mocker.patch('src.controllers.user.login_controller.LoginHandler', login_handler)
    login_handler().__enter__.return_value = mock_login_handler_object
    return mock_login_handler_object


@pytest.fixture
def mock_create_access_token(mocker):
    mock_obj = mocker.Mock()
    mocker.patch('src.controllers.user.login_controller.create_access_token', mock_obj)
    return mock_obj


def application_error():
    raise ApplicationError(code=status.HTTP_401_UNAUTHORIZED, message=LOGIN_APPLICATION_ERROR_MESSAGE)


def database_exception():
    raise DatabaseException(LOGIN_DATABASE_ERROR_MESSAGE)


@pytest.fixture
def mock_object(mocker):
    return mocker.Mock()


def test_login_with_correct_data(mock_object, mock_login_handler, mock_create_access_token, admin_test_data):

    auth_data = {
        'user_id': admin_test_data['user_id'],
        'role': 'admin'
    }

    mock_login_handler.login.return_value = auth_data
    mock_create_access_token.return_value = SAMPLE_TOKEN

    expected_return_value = {
        'access_token': SAMPLE_TOKEN
    }

    assert LoginController.login(mock_object) == expected_return_value


def test_login_with_incorrect_credentials(mock_object, mock_login_handler):
    mock_login_handler.login = application_error
    with pytest.raises(HTTPException):
        LoginController.login(mock_object)


def test_login_with_database_exception(mock_object, mock_login_handler):
    mock_login_handler.login = database_exception
    with pytest.raises(HTTPException):
        LoginController.login(mock_object)
