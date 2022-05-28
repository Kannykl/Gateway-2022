"""Database init"""
from fastapi import Request


class BaseRepository:
    """BaseRepo for others instance repositories"""

    def __init__(self, request: Request):
        """Connect to database."""
        self.database = request.app.mongodb
