from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.database import Base


class Season(Base):
    """Season model representing a Formula 1 season"""

    __tablename__ = "seasons"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    year = Column(Integer, unique=True, nullable=False, index=True)
    wikipedia_url = Column(String, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    races = relationship("Race", back_populates="season", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Season(year={self.year})>"
