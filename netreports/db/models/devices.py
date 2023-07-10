"""Device related models."""
from datetime import datetime
from pydantic import BaseModel  # pylint: disable=no-name-in-module

from netreports.schemas import choices


class Device(BaseModel):  # pylint: disable=too-few-public-methods
    """Device model for DB."""

    name: str
    model: str
    site: str
    role: choices.DeviceRole
    lastupdate: datetime
