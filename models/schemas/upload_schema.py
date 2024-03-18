"""Module for upload schema"""
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from fastapi_jsonapi.schema_base import BaseModel, Field, RelationshipInfo

if TYPE_CHECKING:
    from models.schemas.series_schema import SeriesSchema
    from models.schemas.fund_schema import FundSchema


class UploadAttributesBaseSchema(BaseModel):
    """Upload attributes base schema"""
    date: str
    currency: str
    status: str
    agency: str
    error: Optional[str] = None
    approvedBy: Optional[str] = None
    approvalMethod: Optional[str] = None
    publishedBy: Optional[str] = None
    s3Id: Optional[str] = None
    fundId: int
    traceId: str

    series: List["SeriesSchema"] = Field(
        relationship=RelationshipInfo(
            resource_type="series",
            many=True,
        ),
    )
    fund: "FundSchema" = Field(
        relationship=RelationshipInfo(
            resource_type="fund",
        ),
    )


class UploadSchema(UploadAttributesBaseSchema):
    """Upload base schema."""

    class Config:
        """Pydantic model config."""
        orm_mode = True

    id: int
    createdAt: Optional[datetime] = Field(description="Create datetime")
    updatedAt: Optional[datetime] = Field(description="Update datetime")
