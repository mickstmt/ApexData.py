from pydantic import BaseModel
from datetime import datetime


class ConstructorBase(BaseModel):
    """Base schema for Constructor"""
    constructor_id: str
    name: str
    nationality: str
    url: str | None = None


class ConstructorCreate(ConstructorBase):
    """Schema for creating a new Constructor"""
    pass


class ConstructorUpdate(BaseModel):
    """Schema for updating a Constructor"""
    constructor_id: str | None = None
    name: str | None = None
    nationality: str | None = None
    url: str | None = None


class ConstructorResponse(ConstructorBase):
    """Schema for Constructor response"""
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
