import enum
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, DateTime, Enum, ForeignKey
)
from sqlalchemy.orm import relationship
from src.models.mysql.settings.base import Base



class OutcomeEnum(enum.Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class ApprovalsTable(Base):
    __tablename__ = "approvals"

    id = Column(Integer, primary_key=True)
    release_id = Column(Integer, ForeignKey("releases.id"), nullable=False)
    approver_email = Column(String, nullable=False)
    outcome = Column(Enum(OutcomeEnum), nullable=False)
    notes = Column(String)
    timestamp = Column(DateTime, default=datetime)

    release = relationship("Release", back_populates="approvals")
