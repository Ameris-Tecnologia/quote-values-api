"""Module for user schema"""
from fastapi_jsonapi.schema_base import BaseModel


class UserAttributesBaseSchema(BaseModel):
    """User attributes base schema"""
    name: str

    class Config:
        """Config"""
        orm_mode = True


class UserSchema(UserAttributesBaseSchema):
    """User base schema."""
