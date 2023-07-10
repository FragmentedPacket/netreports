"""Store Enums for choices."""
from enum import Enum

# import strawberry


# @strawberry.enum
class CommandParsers(str, Enum):
    """Used to validate correct choice of parser is provided."""

    GENIE = "genie"
    NTC_TEMPLATES = "ntc_templates"
    RAW = "raw"
    TTP = "ttp"
    OTHER = "other"


# @strawberry.enum
class DeviceRole(str, Enum):
    """Valid roles a device may have."""

    ACCESS = "access"
    DATACENTER = "datacenter"
    CORE = "core"
    BRANCH = "branch"
