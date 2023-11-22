import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.player.player import Player


logger = logging.getLogger("main.game")
FINAL_RESULTS = "Your final Score is {0:.2f}"
THANKS_MESSAGE = "Thank You for playing"
SCORED_0_POINTS = "Thank You for playing"


class BaseGame:
    def __init__(self, player) -> None:
        self.player: Player = player

    def declare_final_results(self) -> None:
        print("\n---------------------------------------------------")
        final_score: float = self.player.final_score
        if final_score > 0:
            print("🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊")
            print(FINAL_RESULTS.format(final_score))
        else:
            print("😔😔😔😔😔😔😔😔😔😔😔😔😔😔😔😔😔😔😔😔😔")
            print(SCORED_0_POINTS)
        print("---------------------------------------------------")

    def exit_game(self, rounds_played: int, rounds_won):
        print(THANKS_MESSAGE)
        self.player.update_stats(rounds_played, rounds_won)
