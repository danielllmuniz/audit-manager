from typing import Dict, Tuple
import random
import uuid
from datetime import datetime, timezone
from src.models.mysql.interfaces.release_repository import ReleaseRepositoryInterface
from src.models.mysql.interfaces.application_repository import ApplicationRepositoryInterface
from src.models.mysql.entities.releases import ReleasesTable, EnvironmentEnum, StatusEnum
from src.errors.error_types.http_not_found import HttpNotFoundError
from src.errors.error_types.http_unprocessable_entity import HttpUnprocessableEntityError

class ReleaseCreatorController:
    def __init__(
        self,
        release_repository: ReleaseRepositoryInterface,
        application_repository: ApplicationRepositoryInterface
    ) -> None:
        self.__release_repository = release_repository
        self.__application_repository = application_repository

    def create(self, release_info: Dict) -> Dict:
        application_id = release_info["application_id"]
        version = release_info["version"]
        env = release_info.get("env", "DEV")

        self.__validate_application_exists(application_id)
        env_enum = self.__validate_and_convert_env(env)

        validation_passed, evidence_url, validation_logs = self.__simulate_validation(version)
        initial_status = StatusEnum.PENDING_PREPROD if validation_passed else StatusEnum.REJECTED

        release_created = self.__insert_release_in_db(
            application_id,
            version,
            env_enum,
            evidence_url,
            initial_status,
            validation_logs
        )
        formated_response = self.__format_response(release_created)
        return formated_response

    def __validate_application_exists(self, application_id: int) -> None:
        application = self.__application_repository.get_application(application_id)
        if not application:
            raise HttpNotFoundError(f"Application with id '{application_id}' not found")

    def __validate_and_convert_env(self, env: str) -> EnvironmentEnum:
        try:
            return EnvironmentEnum[env.upper()]
        except KeyError:
            valid_envs = [e.value for e in EnvironmentEnum]
            raise HttpUnprocessableEntityError(f"Invalid environment '{env}'. Valid options: {valid_envs}")

    def __simulate_validation(self, version: str) -> Tuple[bool, str, str]:
        validation_passed = random.random() < 0.8

        evidence_id = str(uuid.uuid4())
        evidence_url = f"https://evidence.example.com/releases/{evidence_id}"

        timestamp = datetime.now(timezone.utc).isoformat()
        if validation_passed:
            logs = f"""
[{timestamp}] Starting automated validation for version {version}
[{timestamp}] Running security checks... PASSED
[{timestamp}] Running code quality analysis... PASSED
[{timestamp}] Running unit tests... PASSED
[{timestamp}] Running integration tests... PASSED
[{timestamp}] All validations passed successfully
[{timestamp}] Evidence stored at: {evidence_url}
[{timestamp}] Release approved for PREPROD
"""
        else:
            logs = f"""
[{timestamp}] Starting automated validation for version {version}
[{timestamp}] Running security checks... PASSED
[{timestamp}] Running code quality analysis... FAILED
[{timestamp}] ERROR: Code quality below threshold
[{timestamp}] ERROR: Found 15 critical issues
[{timestamp}] Validation failed
[{timestamp}] Release REJECTED
"""

        return validation_passed, evidence_url, logs

    def __insert_release_in_db(
        self,
        application_id: int,
        version: str,
        env: EnvironmentEnum,
        evidence_url: str,
        status: StatusEnum,
        validation_logs: str
    ) -> ReleasesTable:
        release_created = self.__release_repository.create_release(
            application_id,
            version,
            env,
            evidence_url,
            status
        )

        release_updated = self.__release_repository.update_release(
            release_created.id,
            {"deployment_logs": validation_logs}
        )

        return release_updated

    def __format_response(self, release_created: ReleasesTable) -> Dict:
        response = {
            "data": {
                "release_id": release_created.id,
                "application_id": release_created.application_id,
                "application_name": release_created.application.name if release_created.application else None,
                "version": release_created.version,
                "env": release_created.env.value,
                "status": release_created.status.value,
                "evidence_url": release_created.evidence_url,
                "validation_logs": release_created.deployment_logs,
                "created_at": release_created.created_at.isoformat()
            }
        }
        return response
