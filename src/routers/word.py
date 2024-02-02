from fastapi import APIRouter, Depends, HTTPException
from fastapi import APIRouter, Depends, HTTPException

from src.DBUtils.game_config.GameConfigDAO import GameConfigDAO
from src.schemas import NewWordSchema, UpdateWordSchema, DeleteWordSchema, WordDifficultySchema
from src.utils.exception import OutOfWordsError, NoSuchWordFoundError
from src.utils.jwt_helper import check_admin, get_token
from src.word_section.words import Words


def get_words_dao():
    return Words()


word_router = APIRouter(prefix='/words', tags=['Words'])

JWT_SECRET = "fIqrMcrIKjZqsEZdfwne82n8YsL6F3K0"
JWT_ALGO = "HS256"


@word_router.get(path='', dependencies=[Depends(check_admin)])
def get(words_dao=Depends(get_words_dao)):
    # Get words
    return words_dao.words


@word_router.post(path='', dependencies=[Depends(check_admin)])
def post(word_data: NewWordSchema, words_dao=Depends(get_words_dao)):
    # New word
    words_dao.add_word_and_write_to_file(**word_data.model_dump())
    return {"message": "Word created successfully."}


@word_router.patch(path='', dependencies=[Depends(check_admin)])
def put(word_data: UpdateWordSchema, words_dao=Depends(get_words_dao)):
    # Update word
    try:
        words_dao.words.update_word_and_write_to_file(**word_data.model_dump())
        return {"message": "Word updated Successfully."}
    except NoSuchWordFoundError:
        raise HTTPException(404, detail="No such word found.")


@word_router.delete(path='', dependencies=[Depends(check_admin)])
def delete(word_data: DeleteWordSchema, words_dao=Depends(get_words_dao)):
    # Delete word
    try:
        words_dao.delete_word_and_write_to_file(**word_data.model_dump())
        return {"message": "Word deleted Successfully."}
    except NoSuchWordFoundError:
        raise HTTPException(404, detail="No such word found.")


@word_router.get(path='/random_word')
def get(word_difficulty_data: WordDifficultySchema, words_dao=Depends(get_words_dao), user=Depends(get_token)):
    difficulty = word_difficulty_data.model_dump()['difficulty']

    with GameConfigDAO() as g_dao:
        # [('EASY', 8),('MEDIUM', 10),('HARD', 12)]
        difficulty_parameters = g_dao.get_difficulty_options()
        difficulty_options = [difficulty_parameter[1] for difficulty_parameter in difficulty_parameters]

    if difficulty not in difficulty_options:
        raise HTTPException(400,
                            detail='Please ensure the difficulty options is according to difficulty options available')

    try:
        random_word = words_dao.get_random_word(difficulty)
        return random_word

    except OutOfWordsError:
        raise HTTPException(500, detail="There was a problem getting a random word. Please try again later.")
