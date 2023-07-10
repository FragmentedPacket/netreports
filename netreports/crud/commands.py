"""API Commands Helper Functions."""
from datetime import datetime

from netreports.db.mongodb import AsyncIOMotorClient
from netreports.schemas.commands import ReturnCommand, CommandBody
from netreports.core import config


async def create_command(conn: MongoClient, device: dict, command: CommandBody) -> ReturnCommand:
    """Create a command entry."""
    command_doc = command.dict()

    command_doc["device_id"] = device["_id"]
    command_doc["site"] = device["site"]
    command_doc["model"] = device["model"]
    command_doc["roles"] = [device["role"]]
    command_doc["lastupdate"] = datetime.now()

    await conn[config.database_name][config.commands_collection_name].insert_one(command_doc)

    return ReturnCommand(**command_doc)


async def delete_command(conn: MongoClient, command_name: str, data_type: str, device_id: str):
    """Delete a device."""
    return await conn[config.database_name][config.commands_collection_name].delete_one(
        {"command": command_name, "data_type": data_type, "device_id": device_id}
    )
