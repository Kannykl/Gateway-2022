from fastapi import Request


class BaseRepository:
    def __init__(self, request: Request):
        """Connect to database."""
        self.database = request.app.mongodb
