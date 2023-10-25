import logging
from Game.game import Game
from os import system
from hangman.graphic import hanged
# from player.player import Player
from word_section.words import WordMachine
from word_section.words import OutOfWordsError
logger = logging.getLogger("main.hangman")


class Hangman(Game):
    """
    This class implements all the game functionalities
    Accepts only one argument of type <Player> during initialisation
    """
    def __init__(self, player):
        super().__init__(player)
        self.left_chances: int = 7
        self.guessed_letters: list[str] = []
        self.correctly_guessed: list[str] = []
        self.current_letter: str | None = None
        self.current_word: str | None = None
        self.current_description: str | None = None
        self.word_machine = WordMachine()

    def get_random_word_and_description(self) -> tuple[str, str]:
        random_word: dict = self.word_machine.get_random_word()
        word = random_word['word']
        description = random_word['hint']
        return word, description

    def reset_game(self) -> None:
        self.left_chances = 7
        self.guessed_letters.clear()
        self.correctly_guessed.clear()
        self.current_word = None
        self.current_letter = None
        self.current_description = None

    def start_game(self) -> None:
        rounds = 2
        print("\n\n")
        print(f"Welcome to game {self.player.name}")
        try:
            while rounds != 0:
                print(f"Round {1 - rounds + 1}")  # It will be total rounds - rounds(var) + 1
                self.current_word, self.current_description = self.get_random_word_and_description()
                score = self.play_game()  # Calls the playing routine for self.player
                self.update_scores(score)  # reflect scores on the players object
                self.results(score, rounds)
                self.reset_game()  # reset hangman variables
                rounds -= 1
            self.declare_results()
        except OutOfWordsError as oe:
            print(oe)
            print("Sorry, Please try again later")

    def play_game(self) -> int:
        while self.left_chances != 0 and not self.all_guessed_correctly():
            self.generate_prompt(self.current_word, self.current_description)
            letter_guessed = Hangman.input_letter()
            while self.is_already_guessed(letter_guessed):
                print("Already Guessed")
                letter_guessed = Hangman.input_letter()
            if not self.validate_input(letter_guessed):
                self.left_chances -= 1
                print(hanged(6-self.left_chances))
            else:
                print("\nCorrect \n")
        print("\n---------------------------------------------------")
        if self.all_guessed_correctly():
            print("Nice Going 👏👏, your word was: ", self.current_word)
        elif self.left_chances == 0:
            print("Dont give up 💪💪, your word was: ", self.current_word)
        return self.left_chances

    def all_guessed_correctly(self) -> bool:
        s1 = set(self.correctly_guessed)
        s2 = set(self.current_word)
        return True if len(s1) == len(s2) else False

    def is_already_guessed(self, letter_guessed) -> bool:
        return True if letter_guessed in self.guessed_letters else False

    def validate_input(self, letter_guessed) -> bool:
        self.guessed_letters.append(letter_guessed)
        if letter_guessed in self.current_word:
            self.correctly_guessed.append(letter_guessed)
            return True
        else:
            return False

    def generate_prompt(self, word, description) -> None:
        print("Word: ", end='\t')
        for ch in word:
            print(ch if ch in self.correctly_guessed else "_", end=' ')
        print("Chances: ", self.left_chances, "/7")
        print("Hint: ", description)

    @staticmethod
    def input_letter() -> str:
        user_input = input("Your guess: ").strip()
        while len(user_input) != 1:
            user_input = input("Please enter a single character: ").strip()
        return user_input

    def update_scores(self, score) -> None:
        """
        Stores the score of the current round in players->score list
        :param score:
        :return: None
        """
        self.player.scores.append(score)

    def results(self, score: int, game_round: int) -> None:
        logger.debug(f"{self.player.name} scored {score}")
        print(f"You scored {score} in Round {game_round}")
        print("---------------------------------------------------")

