from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.database import Base


class RaceResult(Base):
    """RaceResult model representing race results"""

    __tablename__ = "results"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Foreign Keys
    race_id = Column(String, ForeignKey("races.id", ondelete="CASCADE"), nullable=False)
    driver_id = Column(String, ForeignKey("drivers.id", ondelete="RESTRICT"), nullable=False)
    constructor_id = Column(String, ForeignKey("constructors.id", ondelete="RESTRICT"), nullable=False)

    # Result Information
    number = Column(Integer, nullable=False)  # Car number
    grid = Column(Integer, nullable=False)    # Starting grid position
    position = Column(Integer, nullable=True) # Finishing position (null if DNF)
    position_text = Column(String, nullable=False)  # "1", "2", "R" (retired), "D" (disqualified)
    position_order = Column(Integer, nullable=False)  # For sorting
    points = Column(Float, nullable=False, default=0.0)
    laps = Column(Integer, nullable=False)
    time = Column(String, nullable=True)  # Race time for winner, gap for others
    milliseconds = Column(Integer, nullable=True)
    fastest_lap = Column(Integer, nullable=True)  # Lap number of fastest lap
    rank = Column(Integer, nullable=True)  # Rank of fastest lap
    fastest_lap_time = Column(String, nullable=True)
    fastest_lap_speed = Column(Float, nullable=True)
    status = Column(String, nullable=False)  # "Finished", "+1 Lap", "Accident", etc.

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    race = relationship("Race", back_populates="results")
    driver = relationship("Driver", back_populates="results")
    constructor = relationship("Constructor", back_populates="results")

    def __repr__(self):
        return f"<RaceResult(position={self.position}, driver={self.driver_id})>"
