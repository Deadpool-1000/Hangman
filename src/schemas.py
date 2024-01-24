import re
from pydantic import BaseModel, Field, field_validator
pwd_regexp = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$"


class UserSchema(BaseModel):
    uname: str
    password: str = Field(min_length=8)

    @classmethod
    @field_validator("password")
    def regex_match(cls, p: str) -> str:
        re_for_pw: re.Pattern[str] = re.compile(pwd_regexp)
        if not re_for_pw.match(p):
            raise ValueError("invalid password")
        return p


class UserProfileSchema(BaseModel):
    id: str
    uname: str
    high_score: int = Field(min=0)
    total_game: int = Field(min=0)
    total_games_won: int = Field(min=0)
    high_score_created_on: str


class NewWordSchema(BaseModel):
    word: str
    definition: str
    source: str


class UpdateWordSchema(BaseModel):
    new_word: str
    new_definition: str


class DeleteWordSchema(BaseModel):
    word: str


class RandomWordSchema(BaseModel):
    id: str
    part_of_speech: str
    word: str
    hint: str


class LeaderboardSchema(BaseModel):
    uname: str
    high_score: str
    scored_on: str


class ScoreSchema(BaseModel):
    score: int
    total_games_played: int = Field(min=0)
    total_games_won: int = Field(min=0)


class WordDifficultySchema(BaseModel):
    difficulty: int = Field(min=8)
