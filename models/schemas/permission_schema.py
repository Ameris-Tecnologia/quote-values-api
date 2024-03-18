"""Module for permission schema"""
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from fastapi_jsonapi.schema_base import BaseModel, Field, RelationshipInfo

if TYPE_CHECKING:
    from models.schemas.fund_schema import FundSchema


class PermissionAttributesBaseSchema(BaseModel):
    """Permission attributes base schema"""
    email: str
    watch: bool
    approve: bool
    publish: bool
    fundId: int

    fund: "FundSchema" = Field(
        relationship=RelationshipInfo(
            resource_type="fund",
        ),
    )


class PermissionSchema(PermissionAttributesBaseSchema):
    """Permission base schema."""

    class Config:
        """Pydantic model config."""
        orm_mode = True

    id: int
    createdAt: Optional[datetime] = Field(description="Create datetime")
    updatedAt: Optional[datetime] = Field(description="Update datetime")
