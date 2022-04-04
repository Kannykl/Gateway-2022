from pydantic import BaseModel, EmailStr, validator, constr


class User(BaseModel):
    """User representation in database."""
    email: EmailStr
    hashed_password: str
    is_admin: bool = False


class UserIn(BaseModel):
    """User data for registration."""
    email: EmailStr
    password: constr(min_length=8)
    password2: str

    @validator("password2")
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError("passwords don't match")
        return v
