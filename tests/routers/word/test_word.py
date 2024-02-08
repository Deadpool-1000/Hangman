import pytest
from starlette import status
from src.routers.word import check_admin
from src.utils.words_util import word_config
from src.handlers.word.word_handler import word_config as word_config2


NEW_WORD_DATA = {
    "word": "euphemism",
    "definition": "an indirect word or expression that you use instead of a more direct one when you are talking about something that is unpleasant or embarrassing; the use of such expressions",
    "source": "https://languages.oup.com/google-dictionary-hi/"
}


UPDATE_WORD_DATA = {
    "new_word": "euphemism",
    "new_definition": "A feeling of sadness usually for a long time."
}


DELETE_WORD_DATA = {
    "word": "euphemism"
}

DIFFICULTY_DATA = {
    "difficulty": 8
}

TEST_WORD_FILE_PATH = 'tests/data/words.txt'


@pytest.fixture(scope='module', autouse=True)
def override_admin(client):
    client.app.dependency_overrides[check_admin] = lambda: ...


@pytest.fixture(autouse=True)
def patch_word_file_path(monkeypatch):
    monkeypatch.setattr(word_config, 'WORDS_FILE_PATH', TEST_WORD_FILE_PATH)
    monkeypatch.setattr(word_config2, 'WORDS_FILE_PATH', TEST_WORD_FILE_PATH)


@pytest.mark.order(1)
def test_get_all_words(client):
    client.app.dependency_overrides[check_admin] = lambda: ...
    response = client.get('/words')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.order(2)
def test_add_new_word(client):
    response = client.post('/words', json=NEW_WORD_DATA)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.order(4)
def test_update_word(client):
    response = client.put('/words', json=UPDATE_WORD_DATA)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.order(5)
def test_delete_word(client):
    response = client.delete_with_payload(url='/words', json=DELETE_WORD_DATA)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.order(3)
def test_random_word(client):
    response = client.post('/words/random_word', json=DIFFICULTY_DATA)
    print("\n\n----------------------------------", response.json())
    assert response.status_code == status.HTTP_200_OK
