"""Background tasks used by the API."""
from bson.objectid import ObjectId
from pymongo import MongoClient

from netreports.core import config


async def delete_all_commands_for_device(db_client: MongoClient, device_id: ObjectId):
    """When a device is deleted, we need to delete all commands for that device.

    Args:
        db_client (MongoClient): DB Client to interfact with DB
        device_id (ObjectId): The device ID we need to delete all commands for.
    """
    collection = db_client[config.database_name][config.commands_collection_name]
    await collection.delete_many({"device_id": device_id})
