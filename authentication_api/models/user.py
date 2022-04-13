"""User schemas"""
import uuid
from pydantic import BaseModel, EmailStr, validator, constr, Field


class User(BaseModel):
    """User representation in database."""
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    email: EmailStr
    hashed_password: str
    is_admin: bool = False


class UserIn(BaseModel):
    """User data for registration."""
    email: EmailStr
    password: constr(min_length=8)
    password2: str

    @validator("password2")
    def password_match(cls, value, values, **kwargs):
        """Matching passwords"""
        if 'password' in values and value != values['password']:
            raise ValueError("passwords don't match")
        return value
