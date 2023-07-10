"""API Device Helper Functions."""
from typing import Dict
from datetime import datetime

from netreports.db.mongodb import AsyncIOMotorClient
from netreports.schemas.devices import ReturnDevice, DeviceBody
from netreports.core import config


async def get_one_device(conn: MongoClient, query: dict) -> ReturnDevice:
    """Get one device.

    Args:
        conn (MongoClient): MongoDB async client
        query (dict): Mongodb query parameters

    Returns:
        ReturnDevice: Return Device object
    """
    row = await conn[config.database_name][config.devices_collection_name].find_one(query)

    if row:
        return ReturnDevice(**row)


async def get_one_device_raw(conn: MongoClient, query: dict) -> Dict:
    """Get device mongodb object.

    Args:
        conn (MongoClient): MongoDB async client
        query (dict): Mongodb query parameters

    Returns:
        Dict[dict]: Return Device object
    """
    return await conn[config.database_name][config.devices_collection_name].find_one(query)


async def create_device(conn: MongoClient, device: DeviceBody) -> ReturnDevice:
    """Create a device.

    Args:
        conn (MongoClient): MongoDB async client
        device (DeviceBody): Pydantic device object

    Returns:
        ReturnDevice: Return Device object
    """
    device_doc = device.dict()
    device_doc["lastupdate"] = datetime.now()

    await conn[config.database_name][config.devices_collection_name].insert_one(device_doc)

    return ReturnDevice(**device_doc)


async def delete_device(conn: MongoClient, query: dict):
    """Delete a single device.

    Args:
        conn (MongoClient): MongoDB async client
        query (dict): Mongodb query parameters

    Returns:
        _type_: _description_
    """
    return await conn[config.database_name][config.devices_collection_name].delete_one(query)
