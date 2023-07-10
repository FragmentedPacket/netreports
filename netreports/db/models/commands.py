"""Command related models."""
# pylint: disable=too-few-public-methods
from typing import Dict, List, Union
from datetime import datetime
from pydantic import BaseModel  # pylint: disable=no-name-in-module

from netreports.schemas import base, choices


class Command(BaseModel):
    """Command DB model."""

    command: str
    data_type: choices.CommandParsers
    data: Union[Dict, List, str]
    device_id: base.PydanticObjectId
    roles: List[choices.DeviceRole]
    model: str
    site: str
    lastupdate: datetime
