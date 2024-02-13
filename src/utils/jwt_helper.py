import shortuuid
from datetime import timedelta, datetime, timezone
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status

from src.BLOCKLIST import BLOCKLIST
from src.config import get_api_config
from src.config import get_settings

api_config = get_api_config()
ALLOWED_ROLES = [api_config.ADMIN, api_config.PLAYER]
settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='login',
    auto_error=False
)


def verify_token(token):
    try:
        payload = jwt.decode(token, settings.jwt_secret)
        # Revoked token
        if payload['jti'] in BLOCKLIST:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                detail=api_config.TOKEN_REVOKED_MESSAGE
            )

        return payload

    except JWTError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail=api_config.INVALID_JWT_PROVIDED_MESSAGE,
            headers={"WWW-Authenticate": "Bearer"}
        )


def get_token(token: str = Depends(oauth2_scheme)):
    print("token------------> ", token)
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='No JWT Bearer token provided in Authorization header.'
        )
    payload = verify_token(token)
    return payload


def check_admin(payload=Depends(get_token)):
    if payload['role'] != api_config.ADMIN:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=api_config.ADMIN_ONLY_MESSAGE)

    return payload


def create_access_token(payload: dict, expires_delta: timedelta):
    payload.update({
        'jti': api_config.TOKEN_PREFIX + shortuuid.ShortUUID().random(5),
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + expires_delta
    })

    encoded_jwt = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algo)

    return encoded_jwt
