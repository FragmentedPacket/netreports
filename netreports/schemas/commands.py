"""Schemas for commands."""
# pylint: disable=too-few-public-methods

from typing import Dict, List, Union
from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module

from netreports.db.models import commands
from netreports.schemas import base, choices


class CommandBody(BaseModel):
    """Input command structure."""

    command: str
    data_type: choices.CommandParsers
    data: Union[Dict, List, str]

    class Config:
        """API Example Docs."""

        schema_extra = {"example": {"command": "show version", "data_type": "genie", "data": ["version: 4.27.1M"]}}


class ReturnCommand(commands.Command):
    """Return command structure."""

    id: base.PydanticObjectId = Field(default_factory=base.PydanticObjectId, alias="_id")


class ReturnCommandList(BaseModel):
    """Return list from a get multiple."""

    count: int = 0
    results: List[ReturnCommand]
