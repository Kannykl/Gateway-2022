"""User schemas"""
import uuid

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from pydantic import validator


class User(BaseModel):
    """User representation in database."""

    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    email: EmailStr
    hashed_password: str
    is_admin: bool = False


class UserIn(BaseModel):
    """User data for registration."""
    email: EmailStr
    password: str = Field(..., min_length=8, strip_whitespace=True)
    password2: str = Field(..., min_length=8, strip_whitespace=True)
    is_admin: bool = False

    @validator("password2")
    def password_match(cls, value, values, **kwargs):
        """Matching passwords"""
        if "password" in values and value != values["password"]:
            raise ValueError("passwords don't match")
        return value
