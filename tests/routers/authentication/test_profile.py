import pytest

from src.routers.user import get_token


@pytest.fixture
def token_data(common_data):
    return {
        'sub': common_data['admin_id']
    }


def test_get_profile(db_change, admin_test_data, client, token_data):
    client.app.dependency_overrides[get_token] = lambda: token_data
    response = client.get('/users/me')
    assert response.json() == admin_test_data


def test_get_profile_with_invalid_token():
    pass
