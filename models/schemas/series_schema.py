"""Module for series schema"""
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from fastapi_jsonapi.schema_base import BaseModel, Field, RelationshipInfo

if TYPE_CHECKING:
    from models.schemas.upload_schema import UploadSchema


class SeriesAttributesBaseSchema(BaseModel):
    """Series attributes base schema"""
    name: str
    bookValue: str
    status: str
    economicValue: str
    institutionalContributors: int
    issuedQuotes: str
    paidQuotes: str
    netEquity: str
    totalAssets: int
    dataOk: bool
    uploadId: int

    upload: "UploadSchema" = Field(
        relationship=RelationshipInfo(
            resource_type="upload",
        ),
    )


class SeriesSchema(SeriesAttributesBaseSchema):
    """Series base schema."""

    class Config:
        """Pydantic model config."""
        orm_mode = True

    id: int
    createdAt:  Optional[datetime] = Field(description="Create datetime")
    updatedAt:  Optional[datetime] = Field(description="Update datetime")
