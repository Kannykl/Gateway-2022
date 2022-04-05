from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from authentication_api.core.security import verify_password, create_access_token
from authentication_api.models.token import Token, Login
from database_api.endpoints.depends import get_user_repository
from authentication_api.models.user import User, UserIn
from database_api.repositories.users import UserRepository


auth_router = APIRouter()


@auth_router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(log_in: Login, users: UserRepository = Depends(get_user_repository)):
    user = await users.get_by_email(log_in.email)

    if user is None or not verify_password(log_in.password, user.hashed_password):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    return Token(
        access_token=create_access_token({"sub": user.email}), token_type="Bearer"
    )


@auth_router.post(
    "/register",
    response_model=User,
    response_model_exclude={"hashed_password"},
    status_code=status.HTTP_200_OK,
)
async def register(
    user_in: UserIn, users: UserRepository = Depends(get_user_repository)
):
    user_ = await users.get_by_email(user_in.email)

    if user_:
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="This email is busy"
        )

    return await users.create(user_in)