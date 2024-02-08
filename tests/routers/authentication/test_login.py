from fastapi.testclient import TestClient
from starlette import status

from src.app import app


def test_login_route_with_correct_credentials(client, db_change):
    auth_data = {"username": "admin", "password": "Abcdef@2", "grant_type": "password"}
    response = client.post('/login', data=auth_data, headers={"content-type": "application/x-www-form-urlencoded"})
    assert response.status_code == status.HTTP_200_OK
    return response.json()['access_token']


def test_login_route_with_wrong_credentials(client, db_change):
    auth_data = {"username": "wrong_username", "password": "wrong_password@2", "grant_type": "password"}
    response = client.post('/login', data=auth_data, headers={"content-type": "application/x-www-form-urlencoded"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
