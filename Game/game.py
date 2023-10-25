import logging
# from player.player import Player
import os
logger = logging.getLogger("main.game")


class Game:
    def __init__(self, player) -> None:
        self.player = player

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
