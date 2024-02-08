from starlette import status
from src.routers.game_parameters import get_token


def test_game_params(client):
    client.app.dependency_overrides[get_token] = lambda: ...
    response = client.get('/game-params')
    assert response.status_code == status.HTTP_200_OK
