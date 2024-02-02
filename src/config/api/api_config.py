import os

import yaml

path_current_directory = os.path.dirname(__file__)
API_CONFIG_PATH = os.path.join(path_current_directory, 'api.yml')


class ApiConfig:
    ROLE_ADMIN = None
    ROLE_USER = None
    GAME_PARAMS_ROUND = None
    GAME_PARAMS_DIFFICULTY = None
    LOGIN_SUMMARY = None
    INVALID_USERNAME_OR_PASSWORD_MESSAGE = None
    DATABASE_ERROR_MESSAGE = None
    ADMIN = None
    PLAYER = None
    GET_PROFILE_SUMMARY = None
    SIGNUP_SUCCESS_MESSAGE = None
    USERNAME_TAKEN_MESSAGE = None
    APPLICATION_ERROR_MESSAGE = None
    LOGOUT_SUCCESS_MESSAGE = None
    INVALID_ROLE_MESSAGE = None
    INVALID_JWT_PROVIDED_MESSAGE = None
    ADMIN_ONLY_MESSAGE = None
    TOKEN_REVOKED_MESSAGE = None
    TOKEN_PREFIX = None
    PWD_REGEXP = None


    @classmethod
    def load(cls):
        with open(API_CONFIG_PATH, 'r') as f:
            data = yaml.safe_load(f)
            cls.ROLE_ADMIN = data['ROLE_ADMIN']
            cls.ROLE_USER = data['ROLE_USER']
            cls.GAME_PARAMS_ROUND = data['GAME_PARAMS_ROUND']
            cls.GAME_PARAMS_DIFFICULTY = data['GAME_PARAMS_DIFFICULTY']
            cls.LOGIN_SUMMARY= data['LOGIN_SUMMARY']
            cls.INVALID_USERNAME_OR_PASSWORD_MESSAGE = data['INVALID_USERNAME_OR_PASSWORD_MESSAGE']
            cls.DATABASE_ERROR_MESSAGE = data['DATABASE_ERROR_MESSAGE']
            cls.GET_PROFILE_SUMMARY = data['GET_PROFILE_SUMMARY']
            cls.SIGNUP_SUCCESS_MESSAGE = data['SIGNUP_SUCCESS_MESSAGE']
            cls.USERNAME_TAKEN_MESSAGE = data['USERNAME_TAKEN_MESSAGE']
            cls.APPLICATION_ERROR_MESSAGE = data['APPLICATION_ERROR_MESSAGE']
            cls.LOGOUT_SUCCESS_MESSAGE = data['LOGOUT_SUCCESS_MESSAGE']
            cls.INVALID_ROLE_MESSAGE = data['INVALID_ROLE_MESSAGE']
            cls.INVALID_JWT_PROVIDED_MESSAGE = data['INVALID_JWT_PROVIDED_MESSAGE']
            cls.ADMIN_ONLY_MESSAGE = data['ADMIN_ONLY_MESSAGE']
            cls.TOKEN_REVOKED_MESSAGE = data['TOKEN_REVOKED_MESSAGE']
            cls.TOKEN_PREFIX = data['TOKEN_PREFIX']
            cls.PWD_REGEXP = data['PWD_REGEXP']