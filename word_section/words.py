import logging
import random
import math
logger = logging.getLogger('main.words')


class OutOfWordsError(Exception):
    pass


class WordMachine:
    """
        A class that is used for retrieving words from database
    """
    def __init__(self):
        logger.info("Word Section accessed")
        self.words = []
        self.word_set = set()
        self.get_words_list()

    def get_words_list(self):
        with open("word_section/words.txt", 'r') as f:
            temp = [line.split('|') for line in f.readlines()]
            words_dict = [{
               "id": ind,
               "word":  word[0],
               "part_of_speech": word[1],
               "hint": word[2]
            } for ind, word in enumerate(temp) if word[1] == 'noun' and len(word[0]) > 10]
            # print(words_dict[:3])
            self.words = words_dict

    def get_random_word(self):
        # self.words=[]
        if len(self.words) == 0:
            raise OutOfWordsError("No words found!")
            # print("No words available")
            # return
        my_num = math.floor(random.random()*len(self.words))
        while my_num in self.word_set:
            my_num = math.floor(random.random()*len(self.words))
        self.word_set.add(my_num)
        return self.words[my_num]



