from datetime import datetime
from typing import Optional, Dict
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class SampleEntityBase(BaseModel):
    """Base schema for SampleEntity with common fields"""
    required_uuid: UUID = Field(..., description="Required UUID field")
    string_field: str = Field(..., min_length=1, max_length=255, description="Required string field")
    required_jsonb: Dict = Field(..., description="Required JSONB field")
    optional_uuid: Optional[UUID] = Field(None, description="Optional UUID field")
    optional_text: Optional[str] = Field(None, description="Optional text field")
    optional_jsonb: Optional[Dict] = Field(None, description="Optional JSONB field")
    big_int: int = Field(default=1, ge=0, description="Big integer field")


class SampleEntityCreate(SampleEntityBase):
    """Schema for creating a new SampleEntity"""
    pass


class SampleEntityUpdate(BaseModel):
    """Schema for updating an existing SampleEntity (all fields optional)"""
    required_uuid: Optional[UUID] = None
    optional_uuid: Optional[UUID] = None
    string_field: Optional[str] = Field(None, min_length=1, max_length=255)
    optional_text: Optional[str] = None
    required_jsonb: Optional[Dict] = None
    optional_jsonb: Optional[Dict] = None
    big_int: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


class SampleEntityResponse(SampleEntityBase):
    """Schema for SampleEntity response"""
    id: UUID
    is_active: bool
    is_deleted: bool
    created_on: datetime
    modified_on: datetime

    model_config = ConfigDict(from_attributes=True)


class SampleEntityListResponse(BaseModel):
    """Schema for paginated list response"""
    items: list[SampleEntityResponse]
    total: int
    skip: int
    limit: int


class DeleteResponse(BaseModel):
    """Schema for delete operation response"""
    success: bool
    message: str
    id: UUID

