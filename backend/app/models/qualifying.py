from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.database import Base


class Qualifying(Base):
    """Qualifying model representing qualifying session results"""

    __tablename__ = "qualifying"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Foreign Keys
    race_id = Column(String, ForeignKey("races.id", ondelete="CASCADE"), nullable=False)
    driver_id = Column(String, ForeignKey("drivers.id", ondelete="RESTRICT"), nullable=False)
    constructor_id = Column(String, ForeignKey("constructors.id", ondelete="RESTRICT"), nullable=False)

    # Qualifying Information
    number = Column(Integer, nullable=False)  # Car number
    position = Column(Integer, nullable=False)  # Qualifying position
    q1 = Column(String, nullable=True)  # Q1 time
    q2 = Column(String, nullable=True)  # Q2 time
    q3 = Column(String, nullable=True)  # Q3 time

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    race = relationship("Race", back_populates="qualifying")
    driver = relationship("Driver", back_populates="qualifying")

    def __repr__(self):
        return f"<Qualifying(position={self.position}, driver={self.driver_id})>"
