"""Fixtures to use throughout tests."""

# from fastapi.testclient import TestClient
# import asyncio
# import json
# import pytest
#
# from netreports.main import app
# from netreports.core.db.mongodb import get_database
#
# FIXTURES_DIR = "tests/fixtures"
#
#
# @pytest.fixture(scope="session")
# def test_database():
#     db = asyncio.run(get_database())
#     yield db
#
#
# @pytest.fixture(scope="session")
# def test_client():
#     """Return a test client used through testing."""
#     with TestClient(app) as test_client:
#         yield test_client
#
#
# @pytest.fixture(scope="session")
# def get_all_device_docs():
#     """Return get_all_devices.json fixture data."""
#     with open(f"{FIXTURES_DIR}/get_all_devices.json") as file:
#         devices = json.loads(file.read())
#         return len(devices), devices
