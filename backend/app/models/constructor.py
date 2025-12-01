from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.database import Base


class Constructor(Base):
    """Constructor model representing a Formula 1 team/constructor"""

    __tablename__ = "constructors"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    constructor_id = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    nationality = Column(String, nullable=False)
    url = Column(String, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    results = relationship("RaceResult", back_populates="constructor")

    def __repr__(self):
        return f"<Constructor(name={self.name})>"
