from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    jwt_secret: str = "MY_JWT_SECRET_HELLO"
    jwt_algo: str = "HS256"
    env: str = "TEST"


@lru_cache
def get_settings():
    return Settings()
