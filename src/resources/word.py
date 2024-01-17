from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from src.utils.rbac import admin_required
from src.word_section.words import Words
from src.utils.exception import OutOfWordsError, NoSuchWordFoundError
from src.schemas import NewWordSchema, UpdateWordSchema, DeleteWordSchema, RandomWordSchema, WordDifficultySchema
from src.DBUtils.game_config.GameConfigDAO import GameConfigDAO


blp = Blueprint("Words", "words", description="Operation on words")


@blp.route('/word')
class WordsRoute(MethodView):
    init_every_request = False

    def __init__(self):
        self.words = Words()

    @admin_required
    @blp.doc(parameters=[
        {'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>',
         'required': 'true'}])
    def get(self):
        # Get words
        return self.words.words

    @admin_required
    @blp.doc(parameters=[
        {'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>',
         'required': 'true'}])
    @blp.arguments(NewWordSchema)
    def post(self, word_data):
        # New word
        self.words.add_word_and_write_to_file(**word_data)
        return {"message": "Word created successfully."}

    @admin_required
    @blp.doc(parameters=[
        {'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>',
         'required': 'true'}])
    @blp.arguments(UpdateWordSchema)
    def put(self, word_data):
        # Update word
        try:
            self.words.update_word_and_write_to_file(**word_data)
            return {"message": "Word updated Successfully."}
        except NoSuchWordFoundError:
            abort(404, message="No such word found.")

    @admin_required
    @blp.doc(parameters=[
        {'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>',
         'required': 'true'}])
    @blp.arguments(DeleteWordSchema)
    def delete(self, word_data):
        # Delete word
        try:
            self.words.delete_word_and_write_to_file(**word_data)
            return {"message": "Word deleted Successfully."}
        except NoSuchWordFoundError:
            abort(404, message="No such word found.")


@blp.route('/random_word')
class RandomWord(MethodView):
    init_every_request = False

    def __init__(self):
        self.words = Words()

    @jwt_required()
    @blp.doc(parameters=[
        {'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>',
         'required': 'true'}])
    @blp.response(200, RandomWordSchema)
    @blp.arguments(WordDifficultySchema)
    def get(self, word_difficulty_data):
        difficulty = word_difficulty_data['difficulty']

        with GameConfigDAO() as g_dao:
            # [('EASY', 8),('MEDIUM', 10),('HARD', 12)]
            difficulty_parameters = g_dao.get_difficulty_options()
            difficulty_options = [difficulty_parameter[1] for difficulty_parameter in difficulty_parameters]

        if difficulty not in difficulty_options:
            abort(400, message='Please ensure the difficulty options is according to difficulty options available')

        try:
            random_word = self.words.get_random_word(difficulty)
            return random_word

        except OutOfWordsError:
            abort(500, message="There was a problem getting a random word. Please try again later.")
