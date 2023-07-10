"""API Configuration."""
import os
from starlette.datastructures import CommaSeparatedStrings, Secret

from netreports import version

# Python version details
base_dir = os.path.abspath(os.path.dirname(__file__))

API_V1_STR = "/api/v1"

# Project configuration
PROJECT_VERSION = version.__version__
PROJECT_NAME = os.getenv("PROJECT_NAME", version.__title__)
PROJECT_DESCRIPTION = os.getenv("PROJECT_DESCRIPTION", version.__description__)
PROJECT_AUTHOR = version.__author__
PROJECT_EMAIL = version.__email__
PROJECT_LICENSE = version.__license__
PROJECT_LICENSE_URL = "https://www.apache.org/licenses/LICENSE-2.0"
PROJECT_QUERY_LIMIT = 1000

# Fast API Settings
MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", "100"))
MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", "100"))

# FastAPI Auth
SECRET_KEY = Secret(os.getenv("SECRET_KEY", "secret key for project"))

# FastAPI Middleware
ALLOWED_HOSTS = CommaSeparatedStrings(os.getenv("ALLOWED_HOSTS", ""))

# Database configuration
MONGO_HOST = os.getenv("MONGO_HOST", "mongodb")
MONGO_PORT = int(os.getenv("MONGO_PORT", "27017"))
MONGO_USER = os.getenv("MONGO_USER", "admin")
MONGO_PASS = os.getenv("MONGO_PASSWORD", "mongonumberfive")
MONGO_DB = os.getenv("MONGO_DB", "netreports")

MONGODB_URL = f"mongodb://{MONGO_HOST}:{MONGO_PORT}"

database_name = MONGO_DB

devices_collection_name = "devices"
commands_collection_name = "commands"
