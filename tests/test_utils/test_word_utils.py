import pytest
from src.config.words.words_config import WordsConfig
from src.utils.words_util import simple_prompt, view_list_generator, print_words, input_new_word, input_word_and_new_definition, read_words, words_menu


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


sample_words_large = [
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


class TestWordsUtils:
    def test_print_words(self, capsys, monkeypatch):
        expected_print = '''-------------------------------------------
paint - To paint something
driving - To drive something
-------------------------------------------\n'''
        sample_words = [
            {
                'word': 'paint',
                'hint': 'To paint something'
            },
            {
                'word': 'driving',
                'hint': 'To drive something'
            }
        ]
        monkeypatch.setattr(WordsConfig, 'PRINT_FORMATTED_WORD', value='{} - {}')
        print_words(sample_words)
        captured = capsys.readouterr()
        assert captured.out == expected_print

    @pytest.mark.parametrize('data', [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], [1, 2]])
    def test_view_list_generator_with_non_empty_lists(self, data):
        g = view_list_generator(data)
        assert next(g) == data[:3]

    def test_view_list_generator_with_empty_list(self):
        g = view_list_generator([])
        with pytest.raises(StopIteration):
            next(g)

    @pytest.mark.parametrize(('inps', 'expected'), [(('p', 'q', 'a'), 'a'), (('', 'b'), 'b')])
    def test_simple_prompt(self, monkeypatch, inps, expected):
        inps = iter(inps)
        monkeypatch.setattr('builtins.input', lambda _: next(inps))
        ret_val = simple_prompt('test prompt', ('a', 'b', 'c'))
        assert ret_val == expected

    @pytest.mark.parametrize(('word', 'definition', 'source'), [('test1', 'def1', 'source1'), ('test2', 'def2', 'source2')])
    def test_input_new_word(self, monkeypatch, word, definition, source):
        inps = iter([word, definition, source])
        monkeypatch.setattr('src.utils.words_util.get_good_input', lambda a, b: next(inps))
        ret_word, ret_definition, ret_source = input_new_word()
        assert ret_word == word and ret_definition == definition and ret_source == source

    @pytest.mark.parametrize(('word', 'definition'), [('test1', 'def1'), ('test2', 'def2')])
    def test_input_word_and_new_definition(self, monkeypatch, word, definition):
        inps = iter([word, definition])
        monkeypatch.setattr('src.utils.words_util.get_good_input', lambda a, b: next(inps))
        ret_word, ret_definition = input_word_and_new_definition()
        assert ret_word == word and ret_definition == definition

    def test_read_words_with_non_empty_lines(self, mocker):
        lines = ["abide|noun|to remain; continue; stay|http: // www.dictionary.com / browse / abide"]
        mock_open = mocker.MagicMock()
        mocker.patch('builtins.open', lambda a, b: mock_open)
        mock_open.__enter__().readlines.return_value = lines
        ret_val = read_words()
        assert ret_val == [{
            "id": 0,
            "word": "abide",
            "part_of_speech": "noun",
            "hint": "to remain; continue; stay"
        }]

    def test_read_words_with_empty_words(self, mocker):
        lines = []
        mock_open = mocker.MagicMock()
        mocker.patch('builtins.open', lambda a, b: mock_open)
        mock_open.__enter__().readlines.return_value = lines
        with pytest.raises(Exception):
            read_words()

    @pytest.mark.parametrize('inps', [('n', 'n'), ('n', 'y', 'n', 'n'), ('q', 'n')])
    def test_words_menu(self, monkeypatch, inps):
        inps = iter(inps)
        monkeypatch.setattr('builtins.input', lambda _: next(inps))
        monkeypatch.setattr(WordsConfig, 'PRINT_FORMATTED_WORD', '')
        ret_val = words_menu(sample_words, 'test1', 'test2', 'test3')
        assert ret_val is None

    @pytest.mark.parametrize('inps', [('r', 'q', 'n')])
    def test_words_menu_with_dummy_functionality(self, mocker, inps):
        mock_function = mocker.Mock()
        functionality = {
            'r': mock_function
        }
        inps = iter(inps)
        mocker.patch('builtins.input', lambda _: next(inps))
        mocker.patch.object(WordsConfig, 'PRINT_FORMATTED_WORD', '')
        words_menu(sample_words_large, 'test1', 'test2', 'test3', functionality)
        mock_function.assert_called_once()

    @pytest.mark.parametrize('inps', [('n', 'q', 'n')])
    def test_words_menu_with_large_sample(self, mocker, inps):
        inps = iter(inps)
        mocker.patch('builtins.input', lambda _: next(inps))
        mocker.patch.object(WordsConfig, 'PRINT_FORMATTED_WORD', '')
        ret_val = words_menu(sample_words_large, 'test1', 'test2', 'test3')
        assert ret_val is None
