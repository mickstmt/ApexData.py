from sqlalchemy import Column, String, Integer, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.database import Base


class Driver(Base):
    """Driver model representing a Formula 1 driver"""

    __tablename__ = "drivers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    driver_id = Column(String, unique=True, nullable=False, index=True)
    permanent_number = Column(Integer, nullable=True)
    code = Column(String(3), nullable=True, index=True)
    given_name = Column(String, nullable=False)
    family_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=True)
    nationality = Column(String, nullable=False)
    url = Column(String, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    results = relationship("RaceResult", back_populates="driver")
    qualifying = relationship("Qualifying", back_populates="driver")

    def __repr__(self):
        return f"<Driver(code={self.code}, name={self.given_name} {self.family_name})>"
