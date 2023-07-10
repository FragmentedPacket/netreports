"""FastAPI core app."""

from fastapi import FastAPI
from netreports.api import reports
from netreports.core.config import (
    PROJECT_NAME,
    PROJECT_DESCRIPTION,
    PROJECT_VERSION,
    PROJECT_LICENSE,
    PROJECT_LICENSE_URL,
)
from netreports.core.db.mongodb_utils import connect_to_and_setup_mongo, close_mongo_connection


app = FastAPI(
    title=PROJECT_NAME,
    description=PROJECT_DESCRIPTION,
    version=PROJECT_VERSION,
    license_info={"name": PROJECT_LICENSE, "url": PROJECT_LICENSE_URL},
)

app.add_event_handler("startup", connect_to_and_setup_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

# Custom reports that all fall under the /reports/ URL
# New reports will be added under the base reports.router module.
app.include_router(reports.router)
