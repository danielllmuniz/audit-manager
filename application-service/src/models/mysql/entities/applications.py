from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, DateTime
)
from sqlalchemy.orm import relationship
from src.models.mysql.settings.base import Base

class ApplicationsTable(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    owner_team = Column(String, nullable=False)
    repo_url = Column(String)
    created_at = Column(DateTime, default=datetime)

    releases = relationship("Release", back_populates="application")
