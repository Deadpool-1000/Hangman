import yaml
WORDS_CONFIGS_PATH = 'config/words/words.yml'


class WordsConfig:
    WELCOME_TO_WORD_SECTION = None
    OUT_OF_WORDS = None
    INPUT_WORD_MAIN_PROMPT = None
    INPUT_NEW_WORD_PROMPT = None
    INPUT_NEW_WORD_DEFINITION = None
    EMPTY_NEW_WORD = None
    EMPTY_NEW_WORD_DEFINITION = None
    INPUT_NEW_WORD_SOURCE = None
    EMPTY_NEW_WORD_SOURCE = None
    WORDS_FILE_PATH = None
    DELETE_PROMPT = None
    UPDATE_WORD = None
    UPDATE_NEW_DEFINITION = None
    UPDATE_WORD_EMPTY = None
    UPDATE_DEFINITION_EMPTY = None
    SUCCESS_UPDATE = None
    SUCCESS_DELETE = None
    SUCCESS_ADD = None
    PRINT_FORMATTED_WORD = None
    ALL_WORDS_PROMPT = None
    END_OF_WORDS = None
    ALL_WORDS_MENU_PROMPT = None
    INVALID_INPUT = None
    UPDATE_WORD_MAIN_PROMPT = None

    @classmethod
    def load(cls):
        with open(WORDS_CONFIGS_PATH, 'r') as f:
            data = yaml.safe_load(f)
            cls.WELCOME_TO_WORD_SECTION = data['WELCOME_TO_WORD_SECTION']
            cls.OUT_OF_WORDS = data['OUT_OF_WORDS']
            cls.INPUT_WORD_MAIN_PROMPT = data['INPUT_WORD_MAIN_PROMPT']
            cls.INPUT_NEW_WORD_PROMPT = data['INPUT_NEW_WORD_PROMPT']
            cls.INPUT_NEW_WORD_DEFINITION = data['INPUT_NEW_WORD_DEFINITION']
            cls.EMPTY_NEW_WORD = data['EMPTY_NEW_WORD']
            cls.EMPTY_NEW_WORD_DEFINITION = data['EMPTY_NEW_WORD_DEFINITION']
            cls.INPUT_NEW_WORD_SOURCE = data['INPUT_NEW_WORD_SOURCE']
            cls.EMPTY_NEW_WORD_SOURCE = data['EMPTY_NEW_WORD_SOURCE']
            cls.WORDS_FILE_PATH = data['WORDS_FILE_PATH']
            cls.DELETE_PROMPT = data['DELETE_PROMPT']
            cls.UPDATE_WORD = data['UPDATE_WORD']
            cls.UPDATE_NEW_DEFINITION = data['UPDATE_NEW_DEFINITION']
            cls.UPDATE_WORD_EMPTY = data['UPDATE_WORD_EMPTY']
            cls.UPDATE_DEFINITION_EMPTY = data['UPDATE_DEFINITION_EMPTY']
            cls.SUCCESS_UPDATE = data['SUCCESS_UPDATE']
            cls.SUCCESS_DELETE = data['SUCCESS_DELETE']
            cls.SUCCESS_ADD = data['SUCCESS_ADD']
            cls.PRINT_FORMATTED_WORD = data['PRINT_FORMATTED_WORD']
            cls.ALL_WORDS_PROMPT = data['ALL_WORDS_PROMPT']
            cls.END_OF_WORDS = data['END_OF_WORDS']
            cls.ALL_WORDS_MENU_PROMPT = data['ALL_WORDS_MENU_PROMPT']
            cls.INVALID_INPUT = data['INVALID_INPUT']
            cls.UPDATE_WORD_MAIN_PROMPT = data['UPDATE_WORD_MAIN_PROMPT']
