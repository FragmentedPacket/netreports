"""Schemas for devices."""
# pylint: disable=too-few-public-methods
from typing import List
from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module

from netreports.db.models import devices
from netreports.schemas import base, choices


class DeviceBody(BaseModel):
    """Class for a device."""

    name: str
    model: str
    site: str
    role: choices.DeviceRole

    class Config:
        """API Example Docs."""

        schema_extra = {"example": {"name": "device-01", "model": "7280QR2", "site": "datacenter1", "role": "access"}}


class ReturnDevice(devices.Device):
    """Return device with commands."""

    id: base.PydanticObjectId = Field(default_factory=base.PydanticObjectId, alias="_id")


class ReturnDeviceList(BaseModel):
    """Return list from a get multiple."""

    count: int = 0
    results: List[ReturnDevice]
