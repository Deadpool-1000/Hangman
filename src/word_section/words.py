import random
import math
from os import system
from src.utils.utils import menu
from src.utils.exception import OutOfWordsError, NoSuchWordFoundError
from src.config.prompts.prompts_config import PromptConfig
from src.config.words.words_config import WordsConfig
from src.utils.words_util import words_menu, input_new_word, input_word_and_new_definition
from src.utils.words_util import read_words


class Words:
    """
        A class that is used for retrieving words from database
    """
    singleton = 1
    words = []

    def __init__(self):
        self.word_set = set()
        if self.singleton != 0:
            self.words = read_words()
            self.singleton -= 1

    def get_random_word(self, min_limit: int) -> {str: int | str}:
        words_with_min_difficulty = [word for word in self.words if len(word['word']) >= min_limit]

        if len(words_with_min_difficulty) == 0:
            raise OutOfWordsError(WordsConfig.OUT_OF_WORDS)

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
        print(WordsConfig.WELCOME_TO_WORD_SECTION)
        m = menu(prompt=PromptConfig.WORD_SECTION_PROMPT, allowed=['a', 'p', 'u', 'd'])
        for user_choice in m:
            user_function = word_section_functionalities.get(user_choice)
            user_function()

    def print_all_words_available(self):
        all_words_functionalities = {
            'u': self.update_word,
            'd': self.delete_word
        }
        system('cls')
        words_menu(
            words=self.words,
            main_prompt=WordsConfig.ALL_WORDS_PROMPT,
            functionalities=all_words_functionalities,
            continue_prompt='Do you want to see the words again?(y/n): ',
            functionalities_prompt=WordsConfig.ALL_WORDS_MENU_PROMPT
        )

    def add_new_word(self):
        system('cls')
        word, definition, source = input_new_word()

        self.add_word_and_write_to_file(word, definition, source)

        print(WordsConfig.SUCCESS_ADD.format(word))

    def update_word(self):
        system('cls')
        new_word, new_definition = input_word_and_new_definition()

        self.update_word_and_write_to_file(new_word, new_definition)

        print(WordsConfig.SUCCESS_UPDATE.format(new_word, new_definition))

    def delete_word(self):
        system('cls')
        word = input(WordsConfig.DELETE_PROMPT)

        self.delete_word_and_write_to_file(word)

        print(WordsConfig.SUCCESS_DELETE.format(word))

    def add_word_and_write_to_file(self, word, definition, source):

        with open(WordsConfig.WORDS_FILE_PATH, 'a') as f:
            f.write(f'{word}|noun|{definition}|{source}\n')

        # Load new contents
        self.words = read_words()

    def update_word_and_write_to_file(self, new_word, new_definition):
        contents = []
        flag = 0
        with open(WordsConfig.WORDS_FILE_PATH, 'r') as f:
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
            raise NoSuchWordFoundError('No such word found.')

        with open(WordsConfig.WORDS_FILE_PATH, 'w') as f:
            f.writelines(contents)

        # load new contents
        self.words = read_words()

    def delete_word_and_write_to_file(self, word):
        contents = []
        flag = 0
        with open(WordsConfig.WORDS_FILE_PATH, 'r') as f:
            line = 'm'
            while line:
                line = f.readline()
                if line.split('|')[0] == word:
                    flag = 1
                else:
                    contents.append(line)
        if flag == 0:
            raise NoSuchWordFoundError('No such word found.')

        with open(WordsConfig.WORDS_FILE_PATH, 'w') as f:
            f.writelines(contents)

        self.words = read_words()
