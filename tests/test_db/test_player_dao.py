import pytest
import sqlite3
import hashlib
from src.db.players.PlayerDAO import PlayerDAO


@pytest.fixture
def mock_sqlite3_execute(mocker):
    mock_sqllite3 = mocker.patch('src.db.players.PlayerDAO.sqlite3', spec=sqlite3)
    mock_execute = (
        mock_sqllite3
        .connect
        .return_value
        .cursor
        .return_value
        .execute
    )

    return mock_execute


@pytest.fixture
def mock_user(mock_sqlite3_execute):
    mock_sqlite3_execute.return_value = [('a', 'b', 'c')]


@pytest.fixture
def mock_empty_user(mocker, mock_sqlite3_execute):
    m = mocker.Mock()
    mock_sqlite3_execute.return_value = m
    m.fetchall.return_value = []


@pytest.fixture
def mock_execute_for_login(mocker, mock_sqlite3_execute):
    password = "Abcdef@2"
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    ret_values = iter([[('admin', hashed_password, 'admin')], [('admin', 7, 17, 13, '2023-10-25 11:37:54.637963')]])
    m = mocker.Mock()
    m.fetchall = lambda: next(ret_values)
    mock_sqlite3_execute.return_value = m


class TestPlayerDAO:
    def test_signup_fail(self, mock_user):
        with pytest.raises(Exception):
            with PlayerDAO() as p_dao:
                p_dao.signup('ABC', 'ABC')

    def test_signup_success(self, mock_empty_user):
        with PlayerDAO() as p_dao:
            p_dao.signup('ABC', 'ABC')

    def test_login_fail(self, mock_empty_user):
        with pytest.raises(Exception):
            with PlayerDAO() as p_dao:
                p_dao.login('ABC', 'ABC')

    def test_login_success(self, mock_execute_for_login):
        with PlayerDAO() as p_dao:
            p_tuple = p_dao.login('admin', 'Abcdef@2')
            assert p_tuple.name == 'admin'

    @pytest.mark.parametrize(('uname', 'password'), [('admin', 'aaaaa'), ('aaa', 'aaaaa')])
    def test_login_with_wrong(self, mock_execute_for_login, uname, password):
        with pytest.raises(Exception):
            with PlayerDAO() as p_dao:
                p_dao.login(uname, password)
