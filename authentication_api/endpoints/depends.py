from fastapi import HTTPException, Depends
from pydantic import EmailStr
from starlette import status

from authentication_api.core.security import JWTBearer, decode_access_token
from authentication_api.models.user import User
from database_api.core.depends import get_user_repository
from database_api.repositories.users import UserRepository


async def get_current_user(
        users: UserRepository = Depends(get_user_repository),
        token: str = Depends(JWTBearer()),
) -> User:
    """Get current user via token."""
    cred_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials are not valid")
    payload = decode_access_token(token)

    if payload is None:
        raise cred_exception

    email: EmailStr = payload.get('sub')

    if email is None:
        raise cred_exception

    user = await users.get_by_email(email=email)

    if user is None:
        raise cred_exception

    return user
