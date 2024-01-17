import os
import config.helper
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from dotenv import load_dotenv

from resources.user import blp as user_blueprint
from resources.word import blp as word_blueprint
from resources.score import blp as score_blueprint
from resources.leaderboard import blp as leaderboard_blueprint
from resources.game_parameters import blp as game_params_blueprint
from src.config.api.api_config import ApiConfig
from src.BLOCKLIST import BLOCKLIST

from src.DBUtils.players.PlayerDAO import PlayerDAO


def create_app():
    load_dotenv()
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Hangman REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    api = Api(app)

    app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET')
    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        with PlayerDAO() as p_dao:
            return {
                "role": ApiConfig.ROLE_ADMIN if p_dao.is_admin(identity) else ApiConfig.ROLE_USER
            }

    @jwt.token_in_blocklist_loader
    def token_in_blocklist_loader(jwt_header, jwt_payload):
        print(BLOCKLIST)
        return jwt_payload['jti'] in BLOCKLIST

    api.register_blueprint(user_blueprint)
    api.register_blueprint(word_blueprint)
    api.register_blueprint(score_blueprint)
    api.register_blueprint(leaderboard_blueprint)
    api.register_blueprint(game_params_blueprint)
    return app
