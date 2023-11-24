import pytest
from src.config.prompts.prompts_config import PromptConfig
from src.db.players.PlayerDAO import PlayerDAO
from src.leaderboard.leaderboard import Leaderboard
from src.utils.named_tuples import Leaderboard as l_tuple
from src.config.leaderboard.leaderboard_config import LeaderBoardConfig


sample_data = [
    l_tuple(uname='Milind', high_score=22, scored_on='2023'),
    l_tuple(uname='ABC', high_score=20, scored_on='2023')
]


def mock_format_date(date):
    return date


@pytest.fixture
def mock_leaderboard(monkeypatch):
    monkeypatch.setattr(PromptConfig, 'DBPATH', 'test.db')
    monkeypatch.setattr(PlayerDAO, 'singleton', 0)
    monkeypatch.setattr(PlayerDAO, 'get_leaderboard', lambda _: sample_data)
    monkeypatch.setattr('src.leaderboard.leaderboard.format_date', lambda date: date)
    leader_board = Leaderboard()
    return leader_board


@pytest.fixture
def mock_empty_leaderboard(monkeypatch):
    monkeypatch.setattr(PromptConfig, 'DBPATH', 'test.db')
    monkeypatch.setattr(PlayerDAO, 'singleton', 0)
    monkeypatch.setattr(PlayerDAO, 'get_leaderboard', lambda _: [])
    monkeypatch.setattr('src.leaderboard.leaderboard.format_date', lambda date: date)
    leader_board = Leaderboard()
    return leader_board


@pytest.fixture
def mock_leaderboard_without_date_patch(monkeypatch):
    monkeypatch.setattr(PromptConfig, 'DBPATH', 'test.db')
    monkeypatch.setattr(PlayerDAO, 'singleton', 0)
    monkeypatch.setattr(PlayerDAO, 'get_leaderboard', lambda _: sample_data)
    leader_board = Leaderboard()
    return leader_board


class TestLeaderboard:
    def test_show_leaderboard_with_sample_data(self, capsys, monkeypatch, mock_leaderboard):
        monkeypatch.setattr(LeaderBoardConfig, 'TOP_MESSAGE', "Here are the top scorers of the game")
        monkeypatch.setattr(LeaderBoardConfig, 'TABLE_HEADER', f"{'Username':20}{'High Score':20}{'Scored On':20}")

        expected_message = f'''Here are the top scorers of the game
\n---------------------------------------------------
{'Username':20}{'High Score':20}{'Scored On':20}
{sample_data[0].uname:20}{str(sample_data[0].high_score):20}{sample_data[0].scored_on:20}
{sample_data[1].uname:20}{str(sample_data[1].high_score):20}{sample_data[1].scored_on:20}
---------------------------------------------------\n'''
        mock_leaderboard.show_leaderboard()
        captured = capsys.readouterr()
        assert captured.out == expected_message

    def test_show_leaderboard_with_empty_data(self, capsys, monkeypatch, mock_empty_leaderboard):
        monkeypatch.setattr(LeaderBoardConfig, 'NO_PLAYER_AVAILABLE_TO_SHOW', 'No Players Available to show')
        mock_empty_leaderboard.show_leaderboard()
        captured = capsys.readouterr()
        assert captured.out == 'No Players Available to show\n'

    def test_show_leaderboard_with_bad_date(self, capsys, monkeypatch, mock_leaderboard_without_date_patch):
        monkeypatch.setattr(LeaderBoardConfig, 'TOP_MESSAGE', "Here are the top scorers of the game")
        monkeypatch.setattr(LeaderBoardConfig, 'TABLE_HEADER', f"{'Username':20}{'High Score':20}{'Scored On':20}")

        expected_message = f'''Here are the top scorers of the game
\n---------------------------------------------------
{'Username':20}{'High Score':20}{'Scored On':20}
There was some problem please try again later\n'''
        mock_leaderboard_without_date_patch.show_leaderboard()
        captured = capsys.readouterr()
        assert captured.out == expected_message
