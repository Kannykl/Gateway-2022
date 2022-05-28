"""Token schemas"""
from pydantic import BaseModel
from pydantic import EmailStr


class Token(BaseModel):
    """Token model."""

    access_token: str
    token_type: str


class Login(BaseModel):
    """Info for login in system."""

    email: EmailStr
    password: str
