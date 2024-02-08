import sqlite3
import shortuuid
import hashlib
import pytest
from fastapi.testclient import TestClient
from datetime import datetime

from src.DBUtils.database.database import queries_config
from src.app import app

# TODO add fixture to create all tables and add test data


class CustomTestClient(TestClient):
    def delete_with_payload(self, **kwargs):
        return self.request(method='DELETE', **kwargs)


@pytest.fixture(scope='session')
def common_data():
    return {
        'date_time': str(datetime.now()),
        'admin_id': "1234admin_id"
    }


@pytest.fixture(scope='session')
def client():
    client = CustomTestClient(app)
    return client


@pytest.fixture(scope='session', autouse=True)
def create_database(common_data):
    conn = sqlite3.connect('tests/data/hangman_test.db')
    cur = conn.cursor()
    print("\n\nCreating tables............")
    cur.execute("CREATE TABLE IF NOT EXISTS auth_table(user_id PRIMARY KEY,uname TEXT UNIQUE, password TEXT, role TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS players(user_id TEXT PRIMARY KEY, high_score REAL, total_game INTEGER, total_games_won INTEGER, high_score_created_on timestamp, FOREIGN KEY (user_id) REFERENCES auth_table(user_id))")
    cur.execute("CREATE TABLE IF NOT EXISTS game_config(config_id INTEGER PRIMARY KEY AUTOINCREMENT, config_name TEXT, config_key TEXT, config_value INTEGER)")
    cur.execute("DELETE FROM players")
    cur.execute("DELETE FROM auth_table")
    pwd = hashlib.sha256("Abcdef@2".encode()).hexdigest()
    cur.execute("INSERT INTO auth_table VALUES(?,?,?,?)", (common_data['admin_id'], 'admin', pwd, 'admin'))
    cur.execute("INSERT INTO players VALUES(?,0.0,0,0,?)", (common_data['admin_id'], common_data['date_time']))
    cur.close()
    conn.commit()
    conn.close()
    yield
    conn = sqlite3.connect('tests/data/hangman_test.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM players")
    cur.execute("DELETE FROM auth_table")
    conn.close()


@pytest.fixture
def db_change(monkeypatch):
    monkeypatch.setattr(queries_config, 'DBPATH', 'tests/data/hangman_test.db')


@pytest.fixture
def admin_test_data(common_data):
    return {
        "user_id": "1234admin_id",
        "uname": "admin",
        "high_score": 0.0,
        "total_game": 0,
        "total_games_won": 0,
        "high_score_created_on": common_data['date_time']
    }

