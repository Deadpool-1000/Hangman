import pytest
from src.config.words.words_config import WordsConfig

import src.utils.words_util as words_util


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
        words_util.print_words(sample_words)
        captured = capsys.readouterr()
        assert captured.out == expected_print

    @pytest.mark.parametrize('data', [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], [1, 2]])
    def test_view_list_generator_with_non_empty_lists(self, data):
        g = words_util.view_list_generator(data)
        assert next(g) == data[:3]

    def test_view_list_generator_with_empty_list(self):
        g = words_util.view_list_generator([])
        with pytest.raises(StopIteration):
            next(g)
