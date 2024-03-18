"""Module for fund schema"""
from typing import TYPE_CHECKING, List
from fastapi_jsonapi.schema_base import BaseModel, Field, RelationshipInfo

if TYPE_CHECKING:
    from models.schemas.upload_schema import UploadSchema
    from models.schemas.permission_schema import PermissionSchema


class FundAttributesBaseSchema(BaseModel):
    """Fund attributes base schema"""
    name: str
    active: bool
    sender: str

    uploads: List["UploadSchema"] = Field(
        relationship=RelationshipInfo(
            resource_type="upload",
            many=True,
        ),
    )

    permissions: List["PermissionSchema"] = Field(
        relationship=RelationshipInfo(
            resource_type="permission",
            many=True,
        ),
    )


class FundSchema(FundAttributesBaseSchema):
    """Fund base schema."""

    class Config:
        """Pydantic model config."""
        orm_mode = True

    id: int
