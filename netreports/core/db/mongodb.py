"""MongoDB database initialization."""

from pymongo import MongoClient


class DataBase:  # pylint: disable=too-few-public-methods
    """Database object."""

    client: MongoClient = None


db = DataBase()


async def get_database() -> MongoClient:
    """Return Async Client."""
    return db.client
