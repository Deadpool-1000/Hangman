from jose import jwt, JWTError
from fastapi import HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from src.BLOCKLIST import BLOCKLIST


JWT_SECRET = "fIqrMcrIKjZqsEZdfwne82n8YsL6F3K0"
JWT_ALGO = "HS256"
ALLOWED_ROLES = ['superman', 'batman']
INVALID_ROLE_MESSAGE = "Invalid role provided"
INVALID_JWT_PROVIDED_MESSAGE = 'Invalid JWT provided'
ADMIN = 'superman'
ADMIN_ONLY_MESSAGE = 'You cannot access this resource.'
TOKEN_REVOKED_MESSAGE = 'Token Revoked.'


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='login'
)


def verify_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET)

        # Revoked token
        if payload['jti'] in BLOCKLIST:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                detail=TOKEN_REVOKED_MESSAGE
            )

        return payload

    except JWTError:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail=INVALID_JWT_PROVIDED_MESSAGE,
            headers={"WWW-Authenticate": "Bearer"}
        )


def get_token(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    return payload


def check_admin(payload=Depends(get_token)):
    if payload['role'] != ADMIN:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ADMIN_ONLY_MESSAGE)

    return payload


def has_token(token=Depends(oauth2_scheme)):
    payload = verify_token(token)
    return payload
