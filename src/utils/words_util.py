from os import system
from typing import Iterable
from src.config.words.words_config import WordsConfig
from src.utils.utils import get_good_input


def print_words(words: list[{str: str}]):
    print('-------------------------------------------')
    for word in words:
        print(WordsConfig.PRINT_FORMATTED_WORD.format(word['word'], word['hint']))
    print('-------------------------------------------')


def words_menu(words, main_prompt, functionalities_prompt, continue_prompt, functionalities=None):
    if functionalities is None:
        functionalities = {}

    while True:
        print(main_prompt)
        words_generator = view_list_generator(words)
        did_quit = False

        for my_words in words_generator:
            print_words(my_words)
            user_choice = simple_prompt(functionalities_prompt, [*functionalities.keys(), 'n', 'q'])
            if user_choice == 'n':
                system('cls')
                continue
            elif user_choice == 'q':
                did_quit = True
                break
            else:
                functionalities.get(user_choice)()
            system('cls')

        if not did_quit:
            print(WordsConfig.END_OF_WORDS)
        user_choice = simple_prompt(continue_prompt, ['y', 'n'])
        if user_choice == 'y':
            system('cls')
            continue
        else:
            break


def view_list_generator(lst):
    length = len(lst)
    i = 0
    page = 1
    counter = 0
    data = []
    while i < length:
        data.append(lst[i])
        counter += 1
        i += 1
        if counter > 2 or i == length:
            print(f'------Page: {page}------')
            page += 1
            yield data
            data = []
            counter = 0


def simple_prompt(prompt, allowed: Iterable) -> str:
    user_choice = input(prompt).strip().lower()

    while user_choice not in allowed:
        user_choice = input(WordsConfig.INVALID_INPUT).strip().lower()

    return user_choice


def input_new_word() -> (str, str, str):
    system('cls')
    print(WordsConfig.INPUT_WORD_MAIN_PROMPT)

    word = get_good_input(WordsConfig.INPUT_NEW_WORD_PROMPT, WordsConfig.EMPTY_NEW_WORD)
    definition = get_good_input(WordsConfig.INPUT_NEW_WORD_DEFINITION, WordsConfig.EMPTY_NEW_WORD_DEFINITION)
    source = get_good_input(WordsConfig.INPUT_NEW_WORD_SOURCE, WordsConfig.EMPTY_NEW_WORD_SOURCE)

    return word, definition, source


def input_word_and_new_definition():
    system('cls')
    print(WordsConfig.UPDATE_WORD_MAIN_PROMPT)

    word = get_good_input(WordsConfig.UPDATE_WORD, WordsConfig.UPDATE_WORD_EMPTY)
    definition = get_good_input(WordsConfig.UPDATE_NEW_DEFINITION, WordsConfig.UPDATE_DEFINITION_EMPTY)

    return word, definition
