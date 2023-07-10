"""API Mongodb Utilities."""
import logging
from pymongo import MongoClient

# import pymongo

from netreports.core.db.mongodb import db
from netreports.core import config


def create_indexes(client: MongoClient, database_name: str = None):  # pylint: disable=W0613
    """Create base application indexes for collections."""
    if not database_name:
        database_name = config.MONGO_DB
    # try:
    #     client[database_name][config.devices_collection_name].create_index(
    #         [("name", pymongo.ASCENDING), ("model", pymongo.ASCENDING)], unique=True
    #     )
    #     client[database_name][config.commands_collection_name].create_index(
    #         [("device_id", pymongo.ASCENDING), ("command", pymongo.ASCENDING), ("data_type", pymongo.ASCENDING)],
    #         unique=True,
    #     )
    #     client[database_name][config.commands_collection_name].create_index([("device_id", pymongo.ASCENDING)])

    #     # Create single indexes for device attributes that will be in both the devices and commands collections
    #     for field in ("model", "site", "role"):
    #         client[database_name][config.commands_collection_name].create_index([(field, pymongo.ASCENDING)])
    #         client[database_name][config.devices_collection_name].create_index([(field, pymongo.ASCENDING)])

    #     # Create full compound index in each collection
    #     compound_index = [("site", pymongo.ASCENDING), ("role", pymongo.ASCENDING), ("model", pymongo.ASCENDING)]
    #     client[database_name][config.commands_collection_name].create_index(compound_index)
    #     client[database_name][config.devices_collection_name].create_index(compound_index)

    # except pymongo.errors.DuplicateKeyError:
    #     logging.info("Indexes already exist!")
    # finally:
    #     logging.info("Indexes have been created!")


async def connect_to_and_setup_mongo():
    """Open MongoDB Connection."""
    logging.info("Connecting to Mongo DB...")
    db.client = MongoClient(
        str(config.MONGODB_URL),
        username=config.MONGO_USER,
        password=config.MONGO_PASS,
        maxPoolSize=config.MAX_CONNECTIONS_COUNT,
        minPoolSize=config.MIN_CONNECTIONS_COUNT,
    )
    logging.info("Connected to Mongo DB!")

    logging.info("Creating indexes for collections!")
    create_indexes(db.client)


async def close_mongo_connection():
    """Close MongoDB Connection."""
    logging.info("Closing connection to Mongo DB...")
    db.client.close()
    logging.info("Connection close to Mongo DB!")
