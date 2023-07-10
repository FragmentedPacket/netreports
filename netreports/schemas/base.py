"""Base return schemas."""
# pylint: disable=too-few-public-methods
from pydantic import BaseModel  # pylint: disable=no-name-in-module
from bson.objectid import ObjectId as BsonObjectId


class Return404(BaseModel):
    """Base return for a 404."""

    message: str


class PydanticObjectId(BsonObjectId):
    """Custom Pydantic ObjectId model to handle BSON ObjectId."""

    @classmethod
    def __get_validators__(cls):
        """Return validate method for pydantic validation."""
        yield cls.validate

    @classmethod
    def validate(cls, value):
        """Validate the passed in object is a BsonObjectId."""
        if isinstance(value, str):
            value = BsonObjectId(value)

        if not isinstance(value, BsonObjectId):
            raise TypeError("ObjectId required")

        return str(value)

    @classmethod
    def __modify_schema__(cls, field_schema):
        """Allow FastAPI to build the proper OpenAPI schema."""
        field_schema.update(type="string")
