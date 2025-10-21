from typing import Dict, Tuple
from datetime import datetime, timezone
import random
from src.models.mysql.interfaces.release_repository import ReleaseRepositoryInterface
from src.models.mysql.entities.releases import ReleasesTable, StatusEnum, EnvironmentEnum
from src.errors.error_types.http_not_found import HttpNotFoundError
from src.errors.error_types.http_unprocessable_entity import HttpUnprocessableEntityError
from src.errors.error_types.http_bad_request import HttpBadRequestError

class ReleasePromoterController:
    def __init__(self, release_repository: ReleaseRepositoryInterface) -> None:
        self.__release_repository = release_repository

    def promote(self, release_id: int, user_role: str) -> Dict:
        self.__validate_user_role(user_role)
        release = self.__get_release(release_id)
        self.__validate_release_status(release)

        deployment_success, deployment_logs = self.__fake_deployment(release)

        release_updated = self.__update_release_after_deployment(
            release_id,
            release,
            deployment_success,
            deployment_logs
        )

        formated_response = self.__format_response(release_updated)
        return formated_response

    def __validate_user_role(self, user_role: str) -> None:
        if user_role != "DEVOPS":
            raise HttpBadRequestError("Only users with DEVOPS role can promote releases")

    def __get_release(self, release_id: int) -> ReleasesTable:
        release = self.__release_repository.get_release(release_id)
        if not release:
            raise HttpNotFoundError(f"Release with id '{release_id}' not found")
        return release

    def __validate_release_status(self, release: ReleasesTable) -> None:
        valid_statuses = [StatusEnum.APPROVED_PREPROD, StatusEnum.APPROVED_PROD]
        if release.status not in valid_statuses:
            raise HttpUnprocessableEntityError(
                f"Release can only be promoted when status is APPROVED_PREPROD or APPROVED_PROD. "
                f"Current status: {release.status.value}"
            )

    def __fake_deployment(self, release: ReleasesTable) -> Tuple[bool, str]:
        """
        Simula um deployment automatizado.
        Retorna: (sucesso: bool, logs: str)
        """
        success = random.random() < 0.9

        target_env = self.__determine_target_environment(release.env)

        if success:
            logs = f"""
[{datetime.now(timezone.utc).isoformat()}] Starting deployment...
[{datetime.now(timezone.utc).isoformat()}] Deploying version {release.version} to {target_env.value}
[{datetime.now(timezone.utc).isoformat()}] Building application...
[{datetime.now(timezone.utc).isoformat()}] Running tests...
[{datetime.now(timezone.utc).isoformat()}] All tests passed
[{datetime.now(timezone.utc).isoformat()}] Deploying to {target_env.value} environment...
[{datetime.now(timezone.utc).isoformat()}] Deployment successful!
"""
        else:
            logs = f"""
[{datetime.now(timezone.utc).isoformat()}] Starting deployment...
[{datetime.now(timezone.utc).isoformat()}] Deploying version {release.version} to {target_env.value}
[{datetime.now(timezone.utc).isoformat()}] Building application...
[{datetime.now(timezone.utc).isoformat()}] ERROR: Build failed
[{datetime.now(timezone.utc).isoformat()}] Deployment failed!
"""

        return success, logs

    def __determine_target_environment(self, current_env: EnvironmentEnum) -> EnvironmentEnum:
        """
        Determina o ambiente alvo baseado no ambiente atual.
        DEV -> PREPROD
        PREPROD -> PROD
        """
        env_mapping = {
            EnvironmentEnum.DEV: EnvironmentEnum.PREPROD,
            EnvironmentEnum.PREPROD: EnvironmentEnum.PROD
        }
        return env_mapping.get(current_env, current_env)

    def __determine_new_status(self, current_status: StatusEnum, deployment_success: bool) -> StatusEnum:
        """
        Determina o novo status baseado no status atual e resultado do deployment.
        """
        if not deployment_success:
            return StatusEnum.REJECTED

        if current_status == StatusEnum.APPROVED_PREPROD:
            return StatusEnum.PENDING_PROD
        elif current_status == StatusEnum.APPROVED_PROD:
            return StatusEnum.DEPLOYED

        return current_status

    def __update_release_after_deployment(
        self,
        release_id: int,
        release: ReleasesTable,
        deployment_success: bool,
        deployment_logs: str
    ) -> ReleasesTable:
        """
        Atualiza a release após o deployment.
        """
        update_data = {
            "deployment_logs": deployment_logs,
            "status": self.__determine_new_status(release.status, deployment_success)
        }

        if deployment_success:
            target_env = self.__determine_target_environment(release.env)
            update_data["env"] = target_env
            update_data["deployed_at"] = datetime.now(timezone.utc)

            # Save specific deployment timestamps based on target environment
            if target_env == EnvironmentEnum.PREPROD:
                update_data["deployed_preprod_at"] = datetime.now(timezone.utc)
            elif target_env == EnvironmentEnum.PROD:
                update_data["deployed_prod_at"] = datetime.now(timezone.utc)

        release_updated = self.__release_repository.update_release(release_id, update_data)
        return release_updated

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
                "deployed_at": release_updated.deployed_at.isoformat() if release_updated.deployed_at else None,
                "deployed_preprod_at": release_updated.deployed_preprod_at.isoformat() if release_updated.deployed_preprod_at else None,
                "deployed_prod_at": release_updated.deployed_prod_at.isoformat() if release_updated.deployed_prod_at else None
            }
        }
        return response
