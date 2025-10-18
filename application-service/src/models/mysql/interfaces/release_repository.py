from abc import ABC, abstractmethod
from typing import List
from src.models.mysql.entities.releases import ReleasesTable, EnvironmentEnum, StatusEnum

class ReleaseRepositoryInterface(ABC):
    @abstractmethod
    def create_release(
        self,
        application_id: int,
        version: str,
        env: EnvironmentEnum,
        evidence_url: str = None,
        status: StatusEnum = StatusEnum.CREATED
    ) -> ReleasesTable:
        pass

    @abstractmethod
    def get_release(self, release_id: int) -> ReleasesTable:
        pass

    @abstractmethod
    def list_releases(self) -> List[ReleasesTable]:
        pass

    @abstractmethod
    def list_releases_by_application(self, application_id: int) -> List[ReleasesTable]:
        pass
