"""Security operations"""
import datetime

from fastapi import HTTPException
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from jose import jwt
from passlib.context import CryptContext
from starlette import status

from authentication_api.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from authentication_api.core.config import ALGORITHM
from authentication_api.core.config import SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash the password.

    Args:
        password: user password

    Returns:
        hashed password
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password) -> bool:
    """Verify password with hashed password.

    Args:
        password: user password
        hashed_password: hashed user password

    Returns:
        True/False
    """
    return pwd_context.verify(password, hashed_password)


def create_access_token(data: dict) -> str:
    """Create access token.

    Args:
        data: user data

    Returns:
        Access token
    """
    to_encode = data.copy()
    to_encode.update(
        {
            "exp": datetime.datetime.utcnow()
            + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }
    )

    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)


def decode_access_token(token: str):
    """Decode access token

    Args:
        token: access token

    Returns:
        decoded token
    """
    try:
        encoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

    except (jwt.JWSError, jwt.ExpiredSignatureError):
        return None

    return encoded_jwt


class JWTBearer(HTTPBearer):
    """Check the validity of the token."""

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(
            request
        )
        exception = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid auth token"
        )

        if credentials:
            token = decode_access_token(credentials.credentials)

            if token is None:
                raise exception

            return credentials.credentials

        raise exception


async def get_current_user_dependency(security_scopes: SecurityScopes, request: Request):
    """Get current user."""
    client = request.app.async_client

    token = request.cookies["Token"]

    response = await client.get("/auth/get_current_user", headers={
        "Authorization": f"Bearer {token}",
        "security-scopes": security_scopes.scope_str
    })

    if response.status_code == status.HTTP_403_FORBIDDEN:
        raise HTTPException(
            status_code=response.status_code,
            detail="Not enough permissions or invalid token",
        )
    if response.status_code == status.HTTP_401_UNAUTHORIZED:
        raise HTTPException(
            status_code=response.status_code,
            detail="Could not validate credentials",
        )

    return response.json()
