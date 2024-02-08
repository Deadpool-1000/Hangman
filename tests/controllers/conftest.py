import pytest
from starlette import status

from src.utils.exception import ApplicationError, DatabaseException


@pytest.fixture
def application_error(request):
    raise ApplicationError(code=request.param[0], message=request.param[1])


@pytest.fixture
def database_exception(request):
    raise DatabaseException(request.param[0])
