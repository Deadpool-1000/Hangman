from datetime import timedelta, datetime, timezone
import shortuuid
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status

from src.config import ApiConfig
from src.settings import settings
from src.BLOCKLIST import BLOCKLIST

ALLOWED_ROLES = [ApiConfig.ADMIN, ApiConfig.PLAYER]

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='login'
)


def verify_token(token):
    try:
        payload = jwt.decode(token, settings.jwt_secret)

        # Revoked token
        if payload['jti'] in BLOCKLIST:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                detail=ApiConfig.TOKEN_REVOKED_MESSAGE
            )

        return payload

    except JWTError:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail=ApiConfig.INVALID_JWT_PROVIDED_MESSAGE,
            headers={"WWW-Authenticate": "Bearer"}
        )


def get_token(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    return payload


def check_admin(payload=Depends(get_token)):
    if payload['role'] != ApiConfig.ADMIN:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ApiConfig.ADMIN_ONLY_MESSAGE)

    return payload


def has_token(token=Depends(oauth2_scheme)):
    payload = verify_token(token)
    return payload


def create_access_token(payload: dict, expires_delta: timedelta):
    payload.update({
        'jti': ApiConfig.TOKEN_PREFIX + shortuuid.ShortUUID().random(5),
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + expires_delta
    })

    encoded_jwt = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algo)

    return encoded_jwt
