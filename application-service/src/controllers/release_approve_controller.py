from typing import Dict
from src.models.mysql.interfaces.release_repository import ReleaseRepositoryInterface
from src.models.mysql.interfaces.approval_repository import ApprovalRepositoryInterface
from src.models.mysql.entities.releases import ReleasesTable, StatusEnum
from src.models.mysql.entities.approvals import OutcomeEnum
from src.errors.error_types.http_not_found import HttpNotFoundError
from src.errors.error_types.http_unprocessable_entity import HttpUnprocessableEntityError
from src.errors.error_types.http_bad_request import HttpBadRequestError

class ReleaseApproverController:
    def __init__(
        self,
        release_repository: ReleaseRepositoryInterface,
        approval_repository: ApprovalRepositoryInterface
    ) -> None:
        self.__release_repository = release_repository
        self.__approval_repository = approval_repository

    def approve(self, release_id: int, user_role: str, user_email: str) -> Dict:
        self.__validate_user_role(user_role)
        release = self.__get_release(release_id)
        self.__validate_release_status(release)
        new_status = self.__determine_new_status(release.status)
        release_updated = self.__update_release_status(release_id, new_status)
        self.__create_approval_record(release_id, user_email, OutcomeEnum.APPROVED)
        formated_response = self.__format_response(release_updated)
        return formated_response

    def __validate_user_role(self, user_role: str) -> None:
        if user_role != "APPROVER":
            raise HttpBadRequestError("Only users with APPROVER role can approve releases")

    def __get_release(self, release_id: int) -> ReleasesTable:
        release = self.__release_repository.get_release(release_id)
        if not release:
            raise HttpNotFoundError(f"Release with id '{release_id}' not found")
        return release

    def __validate_release_status(self, release: ReleasesTable) -> None:
        valid_statuses = [StatusEnum.PENDING_PREPROD, StatusEnum.PENDING_PROD]
        if release.status not in valid_statuses:
            raise HttpUnprocessableEntityError(
                f"Release can only be approved when status is PENDING_PREPROD or PENDING_PROD. "
                f"Current status: {release.status.value}"
            )

    def __determine_new_status(self, current_status: StatusEnum) -> StatusEnum:
        status_mapping = {
            StatusEnum.PENDING_PREPROD: StatusEnum.APPROVED_PREPROD,
            StatusEnum.PENDING_PROD: StatusEnum.APPROVED_PROD
        }
        return status_mapping[current_status]

    def __update_release_status(self, release_id: int, new_status: StatusEnum) -> ReleasesTable:
        update_data = {"status": new_status}
        release_updated = self.__release_repository.update_release(release_id, update_data)
        return release_updated

    def __create_approval_record(self, release_id: int, approver_email: str, outcome: OutcomeEnum) -> None:
        self.__approval_repository.create_approval(
            release_id=release_id,
            approver_email=approver_email,
            outcome=outcome,
            notes=f"Release {outcome.value.lower()} by approver"
        )

    def __format_response(self, release_updated: ReleasesTable) -> Dict:
        response = {
            "data": {
                "release_id": release_updated.id,
                "application_id": release_updated.application_id,
                "application_name": release_updated.application.name if release_updated.application else None,
                "version": release_updated.version,
                "env": release_updated.env.value,
                "status": release_updated.status.value,
                "evidence_url": release_updated.evidence_url,
                "logs": release_updated.deployment_logs,
                "created_at": release_updated.created_at.isoformat(),
                "deployed_at": release_updated.deployed_at.isoformat() if release_updated.deployed_at else None
            }
        }
        return response
