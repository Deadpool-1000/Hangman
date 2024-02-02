from fastapi.testclient import TestClient
from starlette import status

from src.app import app


client = TestClient(app)


def test_login_route(db_change):
    data = {"username": "admin", "password": "Abcdef@2", "grant_type": "password"}
    response = client.post('/login', data=data, headers={"content-type": "application/x-www-form-urlencoded"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

