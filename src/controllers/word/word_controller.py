from fastapi import HTTPException

from src.DBUtils.database import Database
from src.handlers import GameParamsHandler
from src.handlers import WordHandler
from src.utils.exception import ApplicationError, DatabaseException


class WordController:
    def __init__(self, word_handler: WordHandler):
        self.word_handler = word_handler

    def get_all_words(self):
        return self.word_handler.words

    def add_new_word(self, new_word_data):
        self.word_handler.add_word_and_write_to_file(**new_word_data.model_dump())
        return {"message": "Word created successfully."}

    def delete_word(self, delete_word_data):
        try:
            self.word_handler.delete_word_and_write_to_file(**delete_word_data.model_dump())
            return {"message": "Word deleted Successfully."}
        except ApplicationError as ae:
            raise HTTPException(ae.code, detail=ae.message)

    def update_word(self, update_word_data):
        try:
            self.word_handler.update_word_and_write_to_file(**update_word_data.model_dump())
            return {"message": "Word updated Successfully."}
        except ApplicationError as ae:
            raise HTTPException(ae.code, detail=ae.message)

    def random_word(self, word_difficulty_data):
        difficulty = word_difficulty_data.model_dump()['difficulty']
        try:
            db = Database()
            with GameParamsHandler(db) as game_params_handler:
                difficulty_allowed = game_params_handler.is_difficulty_allowed(difficulty)

                if difficulty_allowed is False:
                    raise ApplicationError(code=400,
                                           message='Please ensure the difficulty options is according to difficulty options available')

                random_word = self.word_handler.get_random_word(difficulty)
                return random_word

        except ApplicationError as ae:
            raise HTTPException(ae.code, detail=ae.message)

        except DatabaseException as db:
            raise HTTPException(500, detail=str(db))
