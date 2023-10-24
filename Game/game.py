import logging
# from player.player import Player
import os
logger = logging.getLogger("main.game")


class Game:
    def __init__(self, player) -> None:
        self.player = player

    def declare_results(self) -> None:
        print("\n", end="")
        print("---------------------------------------------------")
        if sum(self.player.scores) > 0:
            print("🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊🎊")
            print(f"Your final Score is {sum(self.player.scores)}")
        else:
            print("😔😔😔😔😔😔😔😔😔😔😔😔😔😔😔😔😔😔😔😔😔")
            print("You scored 0 points")
