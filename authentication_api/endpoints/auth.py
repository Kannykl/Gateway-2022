"""Authentication endpoints"""

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from starlette import status
from authentication_api.core.security import verify_password, create_access_token,\
    decode_access_token, JWTBearer
from authentication_api.models.token import Token, Login
from authentication_api.models.user import User, UserIn


auth_router = APIRouter()


@auth_router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    responses={401: {"message": JSONResponse}},
)
async def login(request: Request, log_in: Login):
    """Login the user and return the token."""
    async_request = request.app.async_client
    response = await async_request.get(f"/db/get_user_by_email/?email={log_in.email}")

    user = response.json()

    if user is None or not verify_password(log_in.password, user["hashed_password"]):
        return JSONResponse(
            status_code=401, content={"message": "Incorrect username or password"}
        )

    return Token(
        access_token=create_access_token({"sub": user["email"]}), token_type="Bearer"
    )


@auth_router.post(
    "/register",
    response_model=User,
    response_model_exclude={"hashed_password"},
    status_code=status.HTTP_200_OK,
    responses={409: {"message": JSONResponse}},
)
async def register(request: Request, user_in: UserIn):
    """Register users."""
    async_request = request.app.async_client
    response = await async_request.get(f"/db/get_user_by_email/?email={user_in.email}")

    if response.json():
        return JSONResponse(status_code=409, content={"message": "This email is busy"})

    user_data = {"user": jsonable_encoder(user_in)}

    response = await async_request.post("/db/create_user/", json=user_data)
    new_user = User.parse_obj(response.json())

    return new_user


@auth_router.get(
    "/get_current_user",
    response_model=User,
    response_model_exclude={"hashed_password"},
    status_code=status.HTTP_200_OK,
)
async def get_current_user(request: Request, token: str = Depends(JWTBearer())):
    """Get user from token."""
    async_request = request.app.async_client

    cred_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Credentials are not valid"
    )
    payload = decode_access_token(token)

    if payload is None:
        raise cred_exception

    email: EmailStr = payload.get("sub")

    if email is None:
        raise cred_exception

    response = await async_request.get(f"/db/get_user_by_email/?email={email}")
    user = response.json()

    if user is None:
        raise cred_exception

    return user
