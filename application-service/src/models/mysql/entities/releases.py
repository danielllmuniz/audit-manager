import enum
from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Enum
)
from sqlalchemy.orm import relationship
from src.models.mysql.settings.base import Base

class StatusEnum(enum.Enum):
    CREATED = "CREATED"
    PENDING_PREPROD = "PENDING_PREPROD"
    PENDING_PROD = "PENDING_PROD"
    APPROVED_PREPROD = "APPROVED_PREPROD"
    APPROVED_PROD = "APPROVED_PROD"
    REJECTED = "REJECTED"
    DEPLOYED = "DEPLOYED"

class EnvironmentEnum(enum.Enum):
    DEV = "DEV"
    PREPROD = "PREPROD"
    PROD = "PROD"

class ReleasesTable(Base):
    __tablename__ = "releases"

    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    version = Column(String, nullable=False)
    env = Column(Enum(EnvironmentEnum), nullable=False)
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.CREATED)
    evidence_url = Column(String)
    created_at = Column(DateTime, default=datetime)
    deployed_at = Column(DateTime, nullable=True)

    application = relationship("Application", back_populates="releases")
    approvals = relationship("Approval", back_populates="release")
