import logging
from typing import TYPE_CHECKING
from os import system
if TYPE_CHECKING:
    from player.player import Player


logger = logging.getLogger("main.game")


class BaseGame:
    def __init__(self, player) -> None:
        self.player: Player = player

    def declare_results(self) -> None:
        print("\n---------------------------------------------------")
        final_score: float = self.player.final_score
        if final_score > 0:
            print("🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊")
            print(f"Your final Score is {final_score:.2f}")
        else:
            print("😔😔😔😔😔😔😔😔😔😔😔😔😔😔😔😔😔😔😔😔😔")
            print("You scored 0 points")
        print("---------------------------------------------------")

    def exit_game(self, rounds_played: int, rounds_won):
        print("Thank You for playing")
        self.player.update_stats(rounds_played, rounds_won)

    def calculate_rounds_won(self):
        return self.player.calculate_rounds_won()
