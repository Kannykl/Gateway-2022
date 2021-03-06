"""Authentication endpoints"""
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from fastapi import Security
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette import status

from authentication_api.core.security import create_access_token
from authentication_api.core.security import decode_access_token
from authentication_api.core.security import get_current_user_dependency
from authentication_api.core.security import JWTBearer
from authentication_api.core.security import verify_password
from authentication_api.models.token import Login
from authentication_api.models.token import Token
from authentication_api.models.user import User
from authentication_api.models.user import UserIn

from config import logger

auth_router = APIRouter()


@auth_router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    responses={401: {"message": JSONResponse}},
)
async def login(request: Request, response: Response, log_in: Login):
    """Login the user and return the token."""
    async_request = request.app.async_client
    response_ = await async_request.get(
        f"/db/get_user_by_email/?email={log_in.email}"
    )

    user = response_.json()

    if user is None or not verify_password(
        log_in.password, user["hashed_password"]
    ):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Incorrect username or password"},
        )
    logger.info(f"{user['email']} has been logged")

    roles: list[str] = [
        "user",
    ]

    if user["is_admin"]:
        roles: list[str] = [
            "admin",
        ]

    token_data = {"sub": user["email"], "scopes": roles}
    token = create_access_token(token_data)
    response.set_cookie("Token", token, httponly=True)

    return Token(access_token=token, token_type="Bearer")


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
    response = await async_request.get(
        f"/db/get_user_by_email/?email={user_in.email}"
    )

    if response.json():
        return JSONResponse(
            status_code=409, content={"message": "This email is busy"}
        )

    user_data = {"user": jsonable_encoder(user_in)}

    response = await async_request.post("/db/create_user/", json=user_data)
    new_user = User.parse_obj(response.json())

    logger.info(f"New user registered with email {user_in.email}")

    return new_user


@auth_router.get(
    "/get_current_user",
    response_model=User,
    response_model_exclude={"hashed_password"},
    status_code=status.HTTP_200_OK,
)
async def get_current_user(
    request: Request,
    security_scopes: str = Header(default=None),
    token: str = Depends(JWTBearer()),
):
    """Get user from token."""
    async_request = request.app.async_client

    authenticate_value = (
        f'Bearer scope="{security_scopes}"' if security_scopes else "Bearer"
    )

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    payload = decode_access_token(token)
    email: str = payload.get("sub")
    token_scopes = payload.get("scopes", [])

    for scope in security_scopes.split():
        if scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )

    response = await async_request.get(f"/db/get_user_by_email/?email={email}")
    user = response.json()

    if user is None:
        raise credentials_exception

    return user


@auth_router.post(
    "/create_admin",
    response_model=User,
    response_model_exclude={"hashed_password"},
    status_code=status.HTTP_200_OK,
)
async def create_admin(
    request: Request,
    user_in: UserIn,
    _: User = Security(get_current_user_dependency, scopes=["admin"]),
):
    """Create admin"""
    async_request = request.app.async_client
    response = await async_request.get(
        f"/db/get_user_by_email/?email={user_in.email}"
    )

    if response.json():
        return JSONResponse(
            status_code=409, content={"message": "This email is busy"}
        )

    user_data = {"user": jsonable_encoder(user_in)}
    response = await async_request.post("/db/create_user/", json=user_data)
    new_admin = User.parse_obj(response.json())

    return new_admin
