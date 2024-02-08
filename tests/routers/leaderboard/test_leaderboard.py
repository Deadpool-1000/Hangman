from starlette import status
from src.routers.leaderboard import get_token
from tests.routers.authentication.test_login import test_login_route_with_correct_credentials, test_login_route_with_wrong_credentials


def test_get_leaderboard(client, db_change):
    token = test_login_route_with_correct_credentials(client, db_change)
    response = client.get('/leaderboard', headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK


def test_get_leaderboard_with_wrong_credentials(client, db_change):
    pass

