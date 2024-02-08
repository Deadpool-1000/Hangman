import os
from functools import lru_cache

import yaml
from pydantic_settings import BaseSettings

data = dict()
path_current_directory = os.path.dirname(__file__)
API_CONFIG_PATH = os.path.join(path_current_directory, 'api.yml')
with open(API_CONFIG_PATH, 'r') as f:
    print("loading api.yml")
    data.update(yaml.safe_load(f))


class ApiConfig(BaseSettings):
    ADMIN: str = data['ADMIN']
    PLAYER: str = data['PLAYER']
    GAME_PARAMS_ROUND: str = data['GAME_PARAMS_ROUND']
    GAME_PARAMS_DIFFICULTY: str = data['GAME_PARAMS_DIFFICULTY']
    LOGIN_SUMMARY: str = data['LOGIN_SUMMARY']
    INVALID_USERNAME_OR_PASSWORD_MESSAGE: str = data['INVALID_USERNAME_OR_PASSWORD_MESSAGE']
    DATABASE_ERROR_MESSAGE: str = data['DATABASE_ERROR_MESSAGE']
    GET_PROFILE_SUMMARY: str = data['GET_PROFILE_SUMMARY']
    SIGNUP_SUCCESS_MESSAGE: str = data['SIGNUP_SUCCESS_MESSAGE']
    USERNAME_TAKEN_MESSAGE: str = data['USERNAME_TAKEN_MESSAGE']
    APPLICATION_ERROR_MESSAGE: str = data['APPLICATION_ERROR_MESSAGE']
    LOGOUT_SUCCESS_MESSAGE: str = data['LOGOUT_SUCCESS_MESSAGE']
    INVALID_ROLE_MESSAGE: str = data['INVALID_ROLE_MESSAGE']
    INVALID_JWT_PROVIDED_MESSAGE: str = data['INVALID_JWT_PROVIDED_MESSAGE']
    ADMIN_ONLY_MESSAGE: str = data['ADMIN_ONLY_MESSAGE']
    TOKEN_REVOKED_MESSAGE: str = data['TOKEN_REVOKED_MESSAGE']
    TOKEN_PREFIX: str = data['TOKEN_PREFIX']
    PWD_REGEXP: str = data['PWD_REGEXP']


@lru_cache
def get_api_config():
    return ApiConfig()
