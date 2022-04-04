from starlette.config import Config

config = Config(".env")

DATABASE_HOST = config("SI_DATABASE_HOST", default='localhost')
DATABASE_PORT = config("SI_DATABASE_PORT", default=27017)
DATABASE_NAME = config("SI_DATABASE_NAME", default='stat_inc')

