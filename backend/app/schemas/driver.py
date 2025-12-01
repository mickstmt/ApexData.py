from pydantic import BaseModel
from datetime import datetime, date


class DriverBase(BaseModel):
    """Base schema for Driver"""
    driver_id: str
    permanent_number: int | None = None
    code: str | None = None
    given_name: str
    family_name: str
    date_of_birth: date | None = None
    nationality: str
    url: str | None = None


class DriverCreate(DriverBase):
    """Schema for creating a new Driver"""
    pass


class DriverUpdate(BaseModel):
    """Schema for updating a Driver"""
    driver_id: str | None = None
    permanent_number: int | None = None
    code: str | None = None
    given_name: str | None = None
    family_name: str | None = None
    date_of_birth: date | None = None
    nationality: str | None = None
    url: str | None = None


class DriverResponse(DriverBase):
    """Schema for Driver response"""
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
