from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from src.controllers import WordController
from src.handlers.word.word_handler import WordHandler
from src.schemas import NewWordSchema, UpdateWordSchema, DeleteWordSchema, WordDifficultySchema
from src.utils.jwt_helper import check_admin


def get_word_handler():
    return WordHandler()


def get_word_controller(word_handler: Annotated[WordHandler, Depends(get_word_handler)]):
    return WordController(word_handler)


word_router = APIRouter(prefix='/words', tags=['Words'])


@word_router.get(path='', dependencies=[Depends(check_admin)], status_code=status.HTTP_200_OK)
def get(word_controller=Depends(get_word_controller)):
    # Get words
    words = word_controller.get_all_words()
    return words


@word_router.post(path='', dependencies=[Depends(check_admin)], status_code=status.HTTP_201_CREATED)
def post(word_data: NewWordSchema, word_controller=Depends(get_word_controller)):
    # New word
    word_controller.add_new_word(word_data)
    return {"message": "Word created successfully."}


@word_router.put(path='', dependencies=[Depends(check_admin)], status_code=status.HTTP_200_OK)
def put(update_word_data: UpdateWordSchema, word_controller=Depends(get_word_controller)):
    # Update word
    success_message = word_controller.update_word(update_word_data)
    return success_message


@word_router.delete(path='', dependencies=[Depends(check_admin)], status_code=status.HTTP_200_OK)
def delete(delete_word_data: DeleteWordSchema, word_controller=Depends(get_word_controller)):
    # Delete word
    success_message = word_controller.delete_word(delete_word_data)
    return success_message


@word_router.post(path='/random_word', status_code=status.HTTP_200_OK)
def get(word_difficulty_data: WordDifficultySchema, word_controller=Depends(get_word_controller)):
    # Random word
    random_word = word_controller.random_word(word_difficulty_data)
    return random_word
