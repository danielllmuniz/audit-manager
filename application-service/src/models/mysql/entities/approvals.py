import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from src.models.mysql.settings.base import Base

class OutcomeEnum(enum.Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class ApprovalsTable(Base):
    __tablename__ = "approvals"

    id = Column(Integer, primary_key=True)
    release_id = Column(Integer, ForeignKey("releases.id"), nullable=False)
    approver_email = Column(String(255), nullable=False)  # define tamanho
    outcome = Column(Enum(OutcomeEnum, native_enum=False), nullable=False)
    notes = Column(String(1024), nullable=True)           # opcional, define tamanho
    timestamp = Column(DateTime, default=datetime.utcnow)  # use utcnow

    release = relationship("Release", back_populates="approvals")

    def __repr__(self) -> str:
        return (
            f"<Approval(id={self.id}, release_id={self.release_id}, "
            f"approver_email={self.approver_email}, outcome={self.outcome})>"
        )
