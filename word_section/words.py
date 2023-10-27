import logging
import random
import math
from os import system
from utils.utils import menu
from utils.exception import OutOfWordsError

logger = logging.getLogger('main.words')

WELCOME_TO_WORD_SECTION = "Welcome to word section"
WORD_SECTION_PROMPT = """
'a': Add new word
'p': print all words available
'u': update a particular word
'd': delete a particular word
'q': back to admin panel
Your choice: """
OUT_OF_WORDS = "No words found!"
INPUT_WORD_MAIN_PROMPT = "Please enter the following details to add a new word"
INPUT_NEW_WORD_PROMPT = "New Word: "
INPUT_NEW_WORD_DEFINITION = "Enter a hint or definition for the new word: "
EMPTY_NEW_WORD = "New Word can't be empty: "
EMPTY_NEW_WORD_DEFINITION = "A hint must be given for the new word: "
INPUT_NEW_WORD_SOURCE = "A source or url for the new word: "
EMPTY_NEW_WORD_SOURCE = "Source of the new word can't be empty: "
WORDS_FILE_PATH = "./word_section/words.txt"
DELETE_PROMPT = "Enter the word you want to delete: "
UPDATE_WORD = "Enter the word you want to update: "
UPDATE_NEW_DEFINITION = "Enter the new definition: "
UPDATE_WORD_EMPTY = "Word to update can't be empty"
UPDATE_DEFINITION_EMPTY = "New definition cant be empty"
SUCCESS_UPDATE = "Successfully changed the definition of {} to {}"
SUCCESS_DELETE = "Successfully deleted the word {}"
SUCCESS_ADD = "Successfully added the word {}"
PRINT_FORMATTED_WORD = "{} - {}"
ALL_WORDS_PROMPT = "Here are the available words \n"


class WordMachine:
    """
        A class that is used for retrieving words from database
    """

    def __init__(self):
        logger.info("Word Section accessed")
        self.words = []
        self.word_set = set()
        self.read_words()

    def read_words(self):
        with open(WORDS_FILE_PATH, 'r') as f:
            temp = [line.split('|') for line in f.readlines()]
            words = [{
               "id": ind,
               "word":  word[0],
               "part_of_speech": word[1],
               "hint": word[2]
            } for ind, word in enumerate(temp) if word[1] == 'noun']
            logger.debug(f"No of words available:{len(words)}")
            self.words = words

    def get_random_word(self, min_limit: int) -> {str: int | str}:
        words_with_min_difficulty = [word for word in self.words if len(word['word']) >= min_limit]

        if len(words_with_min_difficulty) == 0:
            raise OutOfWordsError(OUT_OF_WORDS)

        # Random word generation
        my_num = math.floor(random.random()*len(words_with_min_difficulty))
        while my_num in self.word_set:
            my_num = math.floor(random.random()*len(words_with_min_difficulty))
        self.word_set.add(my_num)

        return words_with_min_difficulty[my_num]

    def menu(self):
        word_section_functionalities = {
            'a': self.add_new_word,
            'p': self.print_all_words_available,
            'u': self.update_word,
            'd': self.delete_word

        }
        system('cls')
        print(WELCOME_TO_WORD_SECTION)
        m = menu(prompt=WORD_SECTION_PROMPT, allowed=['a', 'p', 'u', 'd'])
        for user_choice in m:
            user_function = word_section_functionalities.get(user_choice)
            user_function()

    def print_all_words_available(self):
        system('cls')
        print(ALL_WORDS_PROMPT)
        for word in self.words[:10]:
            print(PRINT_FORMATTED_WORD.format(word['word'], word['hint']))

    @staticmethod
    def _input_word_and_new_definition():
        word = input(UPDATE_WORD).strip()
        definition = input(UPDATE_NEW_DEFINITION).strip()
        while len(word) == 0:
            word = input(UPDATE_WORD_EMPTY).strip()
        while len(definition) == 0:
            definition = input(UPDATE_DEFINITION_EMPTY).strip()
        return word, definition

    def add_new_word(self):
        system('cls')
        word, definition, source = self._input_new_word()
        with open(WORDS_FILE_PATH, 'a') as f:
            f.write(f'{word}|noun|{definition}|{source}\n')

        print(SUCCESS_ADD.format(word))
        # Load new contents
        self.read_words()

    def update_word(self):
        system('cls')
        new_word, new_definition = self._input_word_and_new_definition()
        contents = []
        flag = 0
        with open(WORDS_FILE_PATH, 'r') as f:
            line = 'm'
            while line:
                line = f.readline()
                if line.split('|')[0] == new_word:
                    word, _, definition, *rest = line.split('|')
                    word = new_word
                    definition = new_definition
                    contents.append("|".join([word, _, definition, *rest]))
                    flag = 1
                else:
                    contents.append(line)
        if flag == 0:
            print("No such word found")
            return

        with open(WORDS_FILE_PATH, 'w') as f:
            f.writelines(contents)

        print(SUCCESS_UPDATE.format(new_word, new_definition))

        # load new contents
        self.read_words()

    def delete_word(self):
        system('cls')
        word = input(DELETE_PROMPT)
        contents = []
        flag = 0
        with open(WORDS_FILE_PATH, 'r') as f:
            line = 'm'
            while line:
                line = f.readline()
                if line.split('|')[0] == word:
                    flag = 1
                else:
                    contents.append(line)
        if flag == 0:
            print("No such word found")
            return

        with open(WORDS_FILE_PATH, 'w') as f:
            f.writelines(contents)

        print(SUCCESS_DELETE.format(word))
        self.read_words()

    @staticmethod
    def _input_new_word() -> (str, str, str):
        system('cls')
        print(INPUT_WORD_MAIN_PROMPT)
        word = input(INPUT_NEW_WORD_PROMPT).strip()
        definition = input(INPUT_NEW_WORD_DEFINITION).strip()
        source = input(INPUT_NEW_WORD_SOURCE).strip()

        while len(word) == 0:
            word = input(EMPTY_NEW_WORD)

        while len(definition) == 0:
            definition = input(EMPTY_NEW_WORD_DEFINITION)

        while len(source) == 0:
            source = input(EMPTY_NEW_WORD_SOURCE)

        return word, definition, source
