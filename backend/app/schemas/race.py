from pydantic import BaseModel
from datetime import datetime, date
from datetime import time as time_type
from typing import Optional


class RaceBase(BaseModel):
    """Base schema for Race"""
    round: int
    race_name: str
    circuit_id: str
    circuit_name: str
    locality: str
    country: str
    date: date
    time: Optional[time_type] = None
    url: Optional[str] = None


class RaceCreate(RaceBase):
    """Schema for creating a new Race"""
    season_id: str


class RaceUpdate(BaseModel):
    """Schema for updating a Race"""
    round: Optional[int] = None
    race_name: Optional[str] = None
    circuit_id: Optional[str] = None
    circuit_name: Optional[str] = None
    locality: Optional[str] = None
    country: Optional[str] = None
    date: Optional[date] = None
    time: Optional[time_type] = None
    url: Optional[str] = None


class RaceResponse(RaceBase):
    """Schema for Race response"""
    id: str
    season_id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
