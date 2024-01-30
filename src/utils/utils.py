import os
from datetime import timedelta, datetime, timezone
from jose import jwt
import shortuuid

JWT_SECRET = "fIqrMcrIKjZqsEZdfwne82n8YsL6F3K0"
TOKEN_PREFIX = "jwt"


def create_access_token(payload: dict, expires_delta: timedelta):
    payload.update({
        'jti': TOKEN_PREFIX + shortuuid.ShortUUID().random(5),
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + expires_delta
    })

    encoded_jwt = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    return encoded_jwt
