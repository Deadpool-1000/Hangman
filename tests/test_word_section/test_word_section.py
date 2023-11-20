import pytest
from src.word_section.words import Words


sample_words = [
    {
        'word': 'actually',
        'hint': 'as an actual or existing fact'
    },
    {
        'word': 'adjustment',
        'hint': 'the act of adjusting; adaptation to a particular condition, position, or purpose'
    },
    {
        'word': 'adjust',
        'hint': 'to change (something) so that it fits, corresponds, or conforms; adapt; accommodate'
    }
]


@pytest.fixture
def word(monkeypatch):
    monkeypatch.setattr('random.random', 0.8)
    word_section = Words()
    monkeypatch.setattr(word_section, 'read_words', lambda _: None)
    monkeypatch.setattr(word_section, 'words', sample_words)
    return word_section


class TestWordSection:
    def test_random_word(self, word):
        word.get_random_word(0)


