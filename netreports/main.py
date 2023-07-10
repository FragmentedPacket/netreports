"""FastAPI core app."""

from fastapi import FastAPI
from netreports.core.api import reports
from netreports.core.config import (
    PROJECT_NAME,
    PROJECT_DESCRIPTION,
    PROJECT_VERSION,
    PROJECT_AUTHOR,
    PROJECT_EMAIL,
    PROJECT_LICENSE,
    PROJECT_LICENSE_URL,
)
from netreports.db.mongodb_utils import connect_to_and_setup_mongo, close_mongo_connection


app = FastAPI(
    title=PROJECT_NAME,
    description=PROJECT_DESCRIPTION,
    version=PROJECT_VERSION,
    contact={"name": PROJECT_AUTHOR, "email": PROJECT_EMAIL},
    license_info={"name": PROJECT_LICENSE, "url": PROJECT_LICENSE_URL},
)

app.add_event_handler("startup", connect_to_and_setup_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(reports.router, prefix="/reports")
# app.include_router(reports.second_router, prefix="/reports")
