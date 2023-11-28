import pytest
import random
from src.word_section.words import Words
from src.config.words.words_config import WordsConfig


TEST_WORD_FILE_PATH = r'tests\test_word_section\my_words.txt'


@pytest.fixture(scope='class')
def populate_word_file():
    yield
    with open(TEST_WORD_FILE_PATH, 'w') as f:
        f.write('''abate|noun|to reduce in amount, degree, intensity, etc.; lessen; diminish|http://www.dictionary.com/browse/abate
abbreviate|noun|to shorten (a word or phrase) by omitting letters, substituting shorter forms, etc., so that the shortened form can represent the whole word or phrase, as ft. for foot, ab. for about, R.I. for Rhode Island, NW for Northwest, or Xn for Christian.|http://www.dictionary.com/browse/abbreviate
abide|noun|to remain; continue; stay|http://www.dictionary.com/browse/abide
''')


sample_words = [
    {
        'id': 0,
        'word': 'abate',
        'hint': 'to reduce in amount, degree, intensity, etc.; lessen; diminish',
        'part_of_speech': 'noun'
    },
    {
        'id': 1,
        'word': 'abbreviate',
        'hint': 'to shorten (a word or phrase) by omitting letters, substituting shorter forms, etc., so that the shortened form can represent the whole word or phrase, as ft. for foot, ab. for about, R.I. for Rhode Island, NW for Northwest, or Xn for Christian.',
        'part_of_speech': 'noun'
    },
    {
        'id': 2,
        'part_of_speech': 'noun',
        'word': 'abide',
        'hint': 'to remain; continue; stay'
    }
]


sample_words1 = [
    {
        'id': 0,
        'word': 'abate',
        'hint': 'to reduce in amount, degree, intensity, etc.; lessen; diminish',
        'part_of_speech': 'noun'
    },
    {
        'id': 1,
        'word': 'abbreviate',
        'hint': 'to shorten (a word or phrase) by omitting letters, substituting shorter forms, etc., so that the shortened form can represent the whole word or phrase, as ft. for foot, ab. for about, R.I. for Rhode Island, NW for Northwest, or Xn for Christian.',
        'part_of_speech': 'noun'
    },
    {
        'id': 2,
        'part_of_speech': 'noun',
        'word': 'abide',
        'hint': 'to remain; continue; stay'
    },
    {
        'id': 3,
        'word': 'coding',
        'hint': 'stressful job',
        'part_of_speech': 'noun'
    }
]

sample_words2 = [

    {
        'id': 0,
        'word': 'abbreviate',
        'hint': 'to shorten (a word or phrase) by omitting letters, substituting shorter forms, etc., so that the shortened form can represent the whole word or phrase, as ft. for foot, ab. for about, R.I. for Rhode Island, NW for Northwest, or Xn for Christian.',
        'part_of_speech': 'noun'
    },
    {
        'id': 1,
        'part_of_speech': 'noun',
        'word': 'abide',
        'hint': 'to remain; continue; stay'
    },
    {
        'id': 2,
        'part_of_speech': 'noun',
        'word': 'coding',
        'hint': 'stressful job'
    }
]

update_sample_words = [

    {
        'id': 0,
        'word': 'abbreviate',
        'hint': 'to shorten (a word or phrase) by omitting letters, substituting shorter forms, etc., so that the shortened form can represent the whole word or phrase, as ft. for foot, ab. for about, R.I. for Rhode Island, NW for Northwest, or Xn for Christian.',
        'part_of_speech': 'noun'
    },
    {
        'id': 1,
        'part_of_speech': 'noun',
        'word': 'abide',
        'hint': 'To Abide'
    },
    {
        'id': 2,
        'part_of_speech': 'noun',
        'word': 'coding',
        'hint': 'stressful job'
    }
]


@pytest.fixture
def words_from_test_file(monkeypatch):
    monkeypatch.setattr(WordsConfig, 'WORDS_FILE_PATH', TEST_WORD_FILE_PATH)
    word_section = Words()
    return word_section


def mock_input_new_word():
    return 'coding', 'stressful job', 'www.google.com'


def mock_input_word_and_new_definition():
    return 'abide', 'To Abide'


@pytest.mark.usefixtures('populate_word_file')
class TestWordSection:
    @pytest.mark.order(1)
    def test_read_words_with_test_file(self, words_from_test_file):
        assert words_from_test_file.words == sample_words

    @pytest.mark.order(2)
    def test_random_word(self, monkeypatch, words_from_test_file):
        monkeypatch.setattr(random, 'random', lambda: 0.7)
        random_word = words_from_test_file.get_random_word(0)
        assert random_word['word'] == 'abide'

    @pytest.mark.order(3)
    def test_add_new_word(self, monkeypatch, words_from_test_file):
        monkeypatch.setattr('src.word_section.words.input_new_word', mock_input_new_word)
        monkeypatch.setattr(WordsConfig, 'SUCCESS_ADD', '')
        words_from_test_file.add_new_word()
        print(words_from_test_file.words)
        assert words_from_test_file.words == sample_words1

    @pytest.mark.order(4)
    def test_delete_word(self, monkeypatch, words_from_test_file):
        monkeypatch.setattr('builtins.input', lambda _: 'abate')
        monkeypatch.setattr(WordsConfig, 'SUCCESS_DELETE', '')
        words_from_test_file.delete_word()
        assert words_from_test_file.words == sample_words2

    @pytest.mark.order(5)
    def test_update_word(self, monkeypatch, words_from_test_file):
        monkeypatch.setattr('src.word_section.words.input_word_and_new_definition', mock_input_word_and_new_definition)
        monkeypatch.setattr(WordsConfig, 'SUCCESS_UPDATE', '{} {}')
        words_from_test_file.update_word()
        assert words_from_test_file.words == update_sample_words
