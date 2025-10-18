from abc import ABC, abstractmethod
from typing import List
from src.models.mysql.entities.applications import ApplicationsTable

class ApplicationRepositoryInterface(ABC):
    @abstractmethod
    def create_application(self, name: str, owner_team: str, repo_url: str = None) -> ApplicationsTable:
        pass

    @abstractmethod
    def get_application(self, application_id: int) -> ApplicationsTable:
        pass

    @abstractmethod
    def get_application_by_name(self, name: str) -> ApplicationsTable:
        pass

    @abstractmethod
    def list_applications(self) -> List[ApplicationsTable]:
        pass

    @abstractmethod
    def delete_application(self, name: str) -> None:
        pass
