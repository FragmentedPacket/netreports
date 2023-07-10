"""API models for ports report."""
from typing import Optional
from pydantic import BaseModel


class PortsBody(BaseModel):
    """Class for incoming API body for ports report."""

    device: str
    ports_total: int
    ports_up: int
    ports_down: int
    ports_shutdown: int
    domain: Optional[str] = None
