import yaml
import os

path_current_directory = os.path.dirname(__file__)
LEADERBOARD_CONFIG_PATH = os.path.join(path_current_directory, 'leaderboard.yml')



class LeaderBoardConfig:
    NO_PLAYER_AVAILABLE_TO_SHOW = None
    TOP_MESSAGE = None
    TABLE_HEADER = None

    @classmethod
    def load(cls):
        with open(LEADERBOARD_CONFIG_PATH, 'r') as f:
            data = yaml.safe_load(f)
            cls.NO_PLAYER_AVAILABLE_TO_SHOW = data['NO_PLAYER_AVAILABLE_TO_SHOW']
            cls.TOP_MESSAGE = data['TOP_MESSAGE']
            cls.TABLE_HEADER = data['TABLE_HEADER']
