"""Integration tests helpers."""
from datetime import datetime
import pytest

# import time
from fastapi.testclient import TestClient

from pymongo import MongoClient
from pymongo import MongoClient

from netreports.core.db.mongodb import db, get_database
from netreports.core.db.mongodb_utils import create_indexes
from netreports.core import config
from netreports.main import app


@pytest.fixture(scope="session")
def test_client():
    """Return a test client used through testing."""
    test_client = TestClient(app)

    return test_client


def override_get_database():
    """Overrides get_database dependency to provide a DBclient."""
    db.client = MongoClient(
        str(config.MONGODB_URL),
        username=config.MONGO_USER,
        password=config.MONGO_PASS,
        maxPoolSize=config.MAX_CONNECTIONS_COUNT,
        minPoolSize=config.MIN_CONNECTIONS_COUNT,
    )
    return db.client


@pytest.fixture(scope="session")
def db_name():
    """Create DB name var."""
    return f"netreports_integration_test_{datetime.now():%Y-%m-%d_%H:%M:%S}"


@pytest.fixture(autouse=True, scope="session")
def setup_and_teardown(db_name):
    """Used to setup DB and DB collections and then remove after testing is completed."""
    db_client = MongoClient(
        str(config.MONGODB_URL),
        username=config.MONGO_USER,
        password=config.MONGO_PASS,
        maxPoolSize=config.MAX_CONNECTIONS_COUNT,
        minPoolSize=config.MIN_CONNECTIONS_COUNT,
    )
    # Set database_name to fixture name to create our temp testing DB
    config.database_name = db_name
    create_indexes(db_client, db_name)

    # This is preventing a race condition with tests running before indexes have fully finished being created
    # This is allowing duplicate command entries causing subsequent tests to fail.
    # index_info = db_client[db_name]["commands"].index_information()
    # while "device_id_1_command_1_data_type_1" not in index_info:
    #     print("Sleeping until unique index has been created.")
    #     time.sleep(0.25)
    #     index_info = db_client[db_name]["commands"].index_information()

    yield

    db_client.drop_database(db_name)


# DB client needs to be instantiated for tests since we can't re-use application DB client.
app.dependency_overrides[get_database] = override_get_database
