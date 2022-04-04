from pydantic import BaseModel


class Bot(BaseModel):
    """Bot representation in database"""
    username: str
    password: str


class BotIn(Bot):
    """Bot data for creating an instance."""
    pass
