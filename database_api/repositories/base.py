from database_api.core.connection import db


class BaseRepository:
    def __init__(self, database: db):
        """Connect to database."""
        self.database = database
