from src.config.words.words_config import get_word_config

word_config = get_word_config()


def read_words():
    print("Words file ----------->", word_config.WORDS_FILE_PATH)
    with open(rf'{word_config.WORDS_FILE_PATH}', 'r') as f:
        temp = [line.split('|') for line in f.readlines()]
        words = [{
            "id": ind,
            "word": word[0],
            "part_of_speech": word[1],
            "hint": word[2]
        } for ind, word in enumerate(temp) if len(word) > 0 and word[1] == 'noun']
        return words
