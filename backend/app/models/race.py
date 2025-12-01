from sqlalchemy import Column, String, Integer, DateTime, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.database import Base


class Race(Base):
    """Race model representing a Formula 1 Grand Prix"""

    __tablename__ = "races"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Foreign Keys
    season_id = Column(String, ForeignKey("seasons.id", ondelete="CASCADE"), nullable=False)

    # Race Information
    round = Column(Integer, nullable=False)
    race_name = Column(String, nullable=False)
    circuit_id = Column(String, nullable=False, index=True)
    circuit_name = Column(String, nullable=False)
    locality = Column(String, nullable=False)
    country = Column(String, nullable=False)

    # Race Date & Time
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=True)

    # URLs
    url = Column(String, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    season = relationship("Season", back_populates="races")
    results = relationship("RaceResult", back_populates="race", cascade="all, delete-orphan")
    qualifying = relationship("Qualifying", back_populates="race", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Race(name={self.race_name}, round={self.round})>"
