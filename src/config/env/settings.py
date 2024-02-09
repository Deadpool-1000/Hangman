from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
load_dotenv()


class Settings(BaseSettings):
    jwt_secret: str = "MY_JWT_SECRET_HELLO"
    jwt_algo: str = "HS256"
    run_env: str = "TEST"


@lru_cache
def get_settings():
    settings = Settings()
    return settings
