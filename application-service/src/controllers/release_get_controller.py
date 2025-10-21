from typing import Dict
from src.models.mysql.interfaces.release_repository import ReleaseRepositoryInterface
from src.models.mysql.entities.releases import ReleasesTable
from src.errors.error_types.http_not_found import HttpNotFoundError


class ReleaseGetController:
    def __init__(self, release_repository: ReleaseRepositoryInterface) -> None:
        self.__release_repository = release_repository

    def get(self, release_id: int) -> Dict:
        release = self.__get_release(release_id)
        formated_response = self.__format_response(release)
        return formated_response

    def __get_release(self, release_id: int) -> ReleasesTable:
        release = self.__release_repository.get_release(release_id)
        if not release:
            raise HttpNotFoundError(f"Release with id '{release_id}' not found")
        return release

    def __format_response(self, release: ReleasesTable) -> Dict:
        # Format approvals
        approvals = []
        if release.approvals:
            approvals = [
                {
                    "id": approval.id,
                    "approver_email": approval.approver_email,
                    "outcome": approval.outcome.value,
                    "notes": approval.notes,
                    "timestamp": approval.timestamp.isoformat()
                }
                for approval in release.approvals
            ]

        response = {
            "data": {
                "release_id": release.id,
                "application_id": release.application_id,
                "application_name": release.application.name if release.application else None,
                "version": release.version,
                "env": release.env.value,
                "status": release.status.value,
                "evidence_url": release.evidence_url,
                "logs": release.deployment_logs,
                "created_at": release.created_at.isoformat(),
                "deployed_at": release.deployed_at.isoformat() if release.deployed_at else None,
                "approvals": approvals
            }
        }
        return response
