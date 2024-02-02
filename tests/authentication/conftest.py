import pytest
from fastapi.testclient import TestClient
from src.DBUtils.database.database import QueriesConfig
from src.app import app


@pytest.fixture
def test_client():
    client = TestClient(app)
    return client


@pytest.fixture
def db_change(monkeypatch):
    monkeypatch.setattr(QueriesConfig, 'DBPATH', '../../tests/data/hangman_test.db')
