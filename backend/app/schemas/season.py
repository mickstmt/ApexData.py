from pydantic import BaseModel
from datetime import datetime


class SeasonBase(BaseModel):
    """Base schema for Season"""
    year: int
    wikipedia_url: str | None = None


class SeasonCreate(SeasonBase):
    """Schema for creating a new Season"""
    pass


class SeasonUpdate(BaseModel):
    """Schema for updating a Season"""
    year: int | None = None
    wikipedia_url: str | None = None


class SeasonResponse(SeasonBase):
    """Schema for Season response"""
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
