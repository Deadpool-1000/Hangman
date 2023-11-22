import pytest
from datetime import datetime
from src.hangman.hangman import Hangman
from src.config.hangman.hangman_config import HangmanConfig
from src.config.logs.logs_config import LogsConfig


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
    player.calculate_rounds_won.return_value = 1
    return player


@pytest.fixture
def hangman_game(mocker, mock_player):
    mocker.patch.object(HangmanConfig, 'ROUND_INFO', new='{}')
    mocker.patch.object(HangmanConfig, 'WELCOME_TO_GAME', new='{}')
    mocker.patch('src.hangman.hangman.Hangman.play_game')
    mocker.patch('src.hangman.hangman.Hangman.results')
    m2 = mocker.patch('src.hangman.hangman.Hangman.get_random_word_and_description')
    m2.return_value = ('a', 'b')
    mocker.patch('src.hangman.hangman.Hangman.declare_final_results')

    h = Hangman(mock_player, 1)
    return h


@pytest.fixture
def hangman_playable_game(mock_player, mocker):
    mocker.patch.object(HangmanConfig, 'WELCOME_TO_GAME', new='')
    mocker.patch.object(HangmanConfig, 'ROUND_INFO', new='')
    mocker.patch.object(HangmanConfig, 'ALREADY_GUESSED', new='')
    mocker.patch.object(HangmanConfig, 'CORRECT_GUESS', new='')
    mocker.patch.object(HangmanConfig, 'ALL_GUESSED_CORRECTLY', new='')
    mocker.patch.object(HangmanConfig, 'NOT_GUESSED_CORRECTLY', new='')
    mocker.patch.object(HangmanConfig, 'RESULT_OF_SINGLE_ROUND', new='')
    mocker.patch.object(LogsConfig, 'OUT_OF_WORDS_ERROR_LOG', new='')
    mocker.patch.object(LogsConfig, 'PLAYER_RESULT_DEBUG', new='')
    mocker.patch('src.hangman.hangman.Hangman.declare_final_results')
    mocker.patch('src.hangman.hangman.Hangman.generate_prompt')
    random_word_mock = mocker.patch('src.hangman.hangman.Hangman.get_random_word_and_description')
    random_word_mock.return_value = ('hello', 'hello')
    h = Hangman(mock_player, 1)
    return h


class TestHangman:
    def test_game_can_be_started(self, hangman_game):
        assert hangman_game.start_game() is None

    def test_start_game_with_fake_score(self, hangman_game, mocker):
        play_game_mock = mocker.patch('src.hangman.hangman.Hangman.play_game')
        play_game_mock.return_value = 2
        exit_game_mock = mocker.patch('src.hangman.hangman.Hangman.exit_game')
        hangman_game.start_game()
        exit_game_mock.assert_called_with(1, 1)

    def test_play_game(self, mocker, hangman_playable_game):
        my_inputs = iter(['a', 'h', 'e', 'l', 'l', 'o'])
        mocker.patch('src.hangman.hangman.Hangman.input_letter', lambda: next(my_inputs))
        results_mock = mocker.patch('src.hangman.hangman.Hangman.results')
        hangman_playable_game.start_game()
        results_mock.assert_called_with(6, 0)
