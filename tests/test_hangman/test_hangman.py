import pytest
from datetime import datetime
from src.hangman.hangman import Hangman
from src.config.hangman.hangman_config import HangmanConfig


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


@pytest.fixture
def mock_player(mocker):
    player = mocker.Mock()
    player.name = 'Player'
    player.role = 'player'
    player.scores = []
    player.all_time_high_score = 7
    player.total_wins = 3
    player.total_games_won = 3
    player.total_games_played = 2
    player.highscore_created_on = datetime.now()
    return player


@pytest.fixture
def hangman_game(mocker, mock_player):
    mocker.patch.object(HangmanConfig, 'ROUND_INFO', new='{}')
    mocker.patch.object(HangmanConfig, 'WELCOME_TO_GAME', new='{}')
    words_mock = mocker.patch('src.hangman.hangman.Words', autospec=True)
    words_mock.return_value.read_words = lambda _: sample_words
    words_mock.return_value.get_random_word = lambda _: 'word'
    mocker.patch('src.hangman.hangman.Hangman.play_game')
    mocker.patch('src.hangman.hangman.Hangman.results')
    m2 = mocker.patch('src.hangman.hangman.Hangman.get_random_word_and_description')
    m2.return_value = ('a', 'b')
    mocker.patch('src.hangman.hangman.Hangman.declare_results')

    h = Hangman(mock_player, 1)
    return h


class TestHangman:
    def test_game_can_be_started(self, hangman_game):
        assert hangman_game.start_game() is None

    def test_start_game_with_fake_score(self, hangman_game, mocker):
        play_game_mock = mocker.patch('src.hangman.hangman.Hangman.play_game')
        play_game_mock.return_value = 2
        m1 = mocker.patch('src.hangman.hangman.Hangman.exit_game')
        hangman_game.start_game()
