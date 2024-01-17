from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    uname = fields.Str(required=True)
    password = fields.Str(required=True, validate=validate.Regexp("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$"))


class UserProfileSchema(Schema):
    id = fields.Str(required=True)
    uname = fields.Str(required=True)
    high_score = fields.Int(required=True)
    total_game = fields.Int(required=True)
    total_games_won = fields.Int(required=True)
    high_score_created_on = fields.Str(required=True)


class NewWordSchema(Schema):
    word = fields.Str(required=True)
    definition = fields.Str(required=True)
    source = fields.Str(required=True)


class UpdateWordSchema(Schema):
    new_word = fields.Str(required=True)
    new_definition = fields.Str(required=True)


class DeleteWordSchema(Schema):
    word = fields.Str(required=True)


class RandomWordSchema(Schema):
    id = fields.Int(required=True)
    part_of_speech = fields.Str(required=True)
    word = fields.Str(required=True)
    hint = fields.Str(required=True)


class LeaderboardSchema(Schema):
    uname = fields.Str(required=True)
    high_score = fields.Int(required=True)
    scored_on = fields.Str(required=True)


class ScoreSchema(Schema):
    score = fields.Int(required=True)
    total_games_played = fields.Int(required=True)
    total_games_won = fields.Int(required=True)


class WordDifficultySchema(Schema):
    difficulty = fields.Int(required=True)
