"""API Configuration."""
import os
from starlette.datastructures import CommaSeparatedStrings, Secret
import tomli

# Python version details
base_dir = os.path.abspath(os.path.dirname(__file__))

with open("pyproject.toml", "rb") as file:
    pyproject = tomli.load(file)
package_info = pyproject["tool"]["poetry"]


# Project configuration
PROJECT_VERSION = package_info["version"]
PROJECT_NAME = package_info["name"].title()
PROJECT_DESCRIPTION = package_info["description"]
PROJECT_LICENSE = package_info["license"]
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
