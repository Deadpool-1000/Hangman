from src.config.words.words_config import WordsConfig


def read_words():
    with open(rf'{WordsConfig.WORDS_FILE_PATH}', 'r') as f:
        temp = [line.split('|') for line in f.readlines()]
        if len(temp) == 0:
            raise Exception('No words available')
        words = [{
           "id": ind,
           "word":  word[0],
           "part_of_speech": word[1],
           "hint": word[2]
        } for ind, word in enumerate(temp) if word[1] == 'noun']
        return words
