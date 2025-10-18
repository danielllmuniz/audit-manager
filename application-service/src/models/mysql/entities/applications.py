from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from src.models.mysql.settings.base import Base
class ApplicationsTable(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)  # define tamanho
    owner_team = Column(String(255), nullable=False)
    repo_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)  # use utcnow, não datetime diretamente

    releases = relationship("Release", back_populates="application")

    def __repr__(self) -> str:
        return f"<Application(id={self.id}, name={self.name}, owner_team={self.owner_team})>"
