from typing import Dict, Tuple
import random
import uuid
import os
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

        validation_passed, evidence_url = self.__simulate_validation(version)
        initial_status = StatusEnum.PENDING_PREPROD if validation_passed else StatusEnum.REJECTED

        release_created = self.__insert_release_in_db(
            application_id,
            version,
            env_enum,
            evidence_url,
            initial_status,
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

    def __simulate_validation(self, version: str) -> Tuple[bool, str]:
        validation_passed = random.random() < 0.8
        evidence_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        timestamp = now.isoformat()

        # Create uploads directory - use absolute path
        uploads_dir = '/app/uploads'
        os.makedirs(uploads_dir, exist_ok=True)

        # Create evidence text file
        filename = f"evidence_{evidence_id}.txt"
        filepath = os.path.join(uploads_dir, filename)

        # Build evidence content with timestamp-based logs
        if validation_passed:
            evidence_content = f"""[{timestamp}] Starting validation for version {version}...
[{timestamp}] Evidence ID: {evidence_id}
[{timestamp}] Running security checks...
[{timestamp}] Security Checks: PASSED (Score: 95/100)
[{timestamp}]   - No critical vulnerabilities found
[{timestamp}]   - All dependencies up to date
[{timestamp}] Running code quality analysis...
[{timestamp}] Code Quality Analysis: PASSED (Score: 85/100)
[{timestamp}]   - Code meets quality standards
[{timestamp}]   - No major code smells detected
[{timestamp}] Running unit tests...
[{timestamp}] Unit Tests: PASSED (150/150)
[{timestamp}]   - All unit tests passed successfully
[{timestamp}]   - Code coverage: 92%
[{timestamp}] Running integration tests...
[{timestamp}] Integration Tests: PASSED (50/50)
[{timestamp}]   - All integration tests passed
[{timestamp}]   - No regression detected
[{timestamp}] ✓ ALL VALIDATIONS PASSED - Release approved for PREPROD
[{timestamp}] Validation completed successfully!
"""
        else:
            evidence_content = f"""[{timestamp}] Starting validation for version {version}...
[{timestamp}] Evidence ID: {evidence_id}
[{timestamp}] Running security checks...
[{timestamp}] Security Checks: PASSED (Score: 95/100)
[{timestamp}]   - No critical vulnerabilities found
[{timestamp}] Running code quality analysis...
[{timestamp}] Code Quality Analysis: FAILED (Score: 45/100)
[{timestamp}]   ✗ Code quality below threshold
[{timestamp}]   ✗ Found 15 critical issues
[{timestamp}]   ✗ Technical debt too high
[{timestamp}] Running unit tests...
[{timestamp}] Unit Tests: FAILED (135/150)
[{timestamp}]   ✗ 15 tests failed
[{timestamp}]   ✗ Code coverage: 68% (below 80% threshold)
[{timestamp}] Running integration tests...
[{timestamp}] Integration Tests: FAILED (42/50)
[{timestamp}]   ✗ 8 integration tests failed
[{timestamp}]   ✗ Regression detected in API endpoints
[{timestamp}] ✗ VALIDATION FAILED - Release REJECTED
[{timestamp}] Validation completed with errors!
"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(evidence_content)

        evidence_url = f"/audit/evidences/{filename}"



        return validation_passed, evidence_url

    def __insert_release_in_db(
        self,
        application_id: int,
        version: str,
        env: EnvironmentEnum,
        evidence_url: str,
        status: StatusEnum,
    ) -> ReleasesTable:
        release_created = self.__release_repository.create_release(
            application_id,
            version,
            env,
            evidence_url,
            status
        )


        return release_created

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
