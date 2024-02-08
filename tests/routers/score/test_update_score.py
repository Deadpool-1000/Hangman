import pytest
from starlette import status

from src.routers.score import get_token

SCORE_UPDATE_DATA = {
    'score': 7,
    'total_games_played': 1,
    'total_games_won': 1
}


@pytest.fixture
def token_data(common_data):
    return {
        'sub': common_data['admin_id']
    }


def test_update_score(client, token_data, db_change, admin_test_data):
    client.app.dependency_overrides[get_token] = lambda: token_data
    response = client.put('/score', json=SCORE_UPDATE_DATA)
    assert response.status_code == status.HTTP_200_OK
