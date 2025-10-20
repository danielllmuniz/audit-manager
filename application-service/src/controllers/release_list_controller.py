from typing import Dict, List
from src.models.mysql.interfaces.release_repository import ReleaseRepositoryInterface
from src.models.mysql.entities.releases import ReleasesTable

class ReleaseListerController:
    def __init__(self, release_repository: ReleaseRepositoryInterface) -> None:
        self.__release_repository = release_repository

    def list(self) -> Dict:
        releases = self.__get_releases_from_db()
        formated_response = self.__format_response(releases)
        return formated_response

    def __get_releases_from_db(self) -> List[ReleasesTable]:
        releases = self.__release_repository.list_releases()
        return releases

    def __format_response(self, releases: List[ReleasesTable]) -> Dict:
        response = {
            "data": [
                {
                    "release_id": release.id,
                    "application_id": release.application_id,
                    "application_name": release.application.name if release.application else None,
                    "version": release.version,
                    "env": release.env.value,
                    "status": release.status.value,
                    "evidence_url": release.evidence_url,
                    "logs": release.deployment_logs,
                    "created_at": release.created_at.isoformat(),
                    "deployed_at": release.deployed_at.isoformat() if release.deployed_at else None
                }
                for release in releases
            ]
        }
        return response
