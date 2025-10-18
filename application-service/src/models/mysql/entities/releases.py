import enum
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text
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
    version = Column(String(255), nullable=False)
    env = Column(Enum(EnvironmentEnum, native_enum=False), nullable=False)
    status = Column(Enum(StatusEnum, native_enum=False), nullable=False, default=StatusEnum.CREATED)
    evidence_url = Column(String(1024), nullable=True)
    deployment_logs = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    deployed_at = Column(DateTime, nullable=True)

    application = relationship("ApplicationsTable", back_populates="releases")
    approvals = relationship("ApprovalsTable", back_populates="release")

    def __repr__(self) -> str:
        return (
            f"<Release(id={self.id}, application_id={self.application_id}, "
            f"version={self.version}, env={self.env}, status={self.status})>"
        )
