"""Security config"""
from starlette.config import Config


config = Config(".env")

ACCESS_TOKEN_EXPIRE_MINUTES = 60
ALGORITHM = "HS256"
SECRET_KEY = config(
    "SI_SECRET_KEY",
    cast=str,
    default="3b5c7e654c10a562a3d1eccfa2b3585f28b6ec23c25d0fe787a69a03b6081df6",
)
