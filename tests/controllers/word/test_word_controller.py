import pytest

from src.controllers import WordController

SAMPLE_WORDS = [
    {
        "id": 13,
        "word": "accent",
        "part_of_speech": "noun",
        "hint": "prominence of a syllable in terms of differential loudness, or of pitch, or length, or of a combination of these."
    },
    {
        "id": 19,
        "word": "account",
        "part_of_speech": "noun",
        "hint": "An account of something"
    }
]


@pytest.fixture
def word_controller(mocker):
    mock_word_handler = mocker.Mock()
    mock_word_handler.words = SAMPLE_WORDS
    return WordController(mock_word_handler)


def test_get_all_words(word_controller):
    assert word_controller.get_all_words() == SAMPLE_WORDS
