from collections import namedtuple

Player = namedtuple("Player", (
'id', 'name', 'role', 'high_score', 'highscore_created_on', 'total_games_played', 'total_games_won'))
