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
        timestamp = datetime.now(timezone.utc).isoformat()

        # Create uploads directory - use absolute path
        uploads_dir = '/app/uploads'
        os.makedirs(uploads_dir, exist_ok=True)

        # Create evidence text file
        filename = f"evidence_{evidence_id}.txt"
        filepath = os.path.join(uploads_dir, filename)

        # Build evidence content
        if validation_passed:
            test_results = """
1. Security Checks ............................ PASSED (Score: 95/100)
   - No critical vulnerabilities found
   - All dependencies up to date

2. Code Quality Analysis ...................... PASSED (Score: 85/100)
   - Code meets quality standards
   - No major code smells detected

3. Unit Tests ................................. PASSED (150/150)
   - All unit tests passed successfully
   - Code coverage: 92%

4. Integration Tests .......................... PASSED (50/50)
   - All integration tests passed
   - No regression detected
"""
            conclusion = "✓ ALL VALIDATIONS PASSED - Release approved for PREPROD"
        else:
            test_results = """
1. Security Checks ............................ PASSED (Score: 95/100)
   - No critical vulnerabilities found

2. Code Quality Analysis ...................... FAILED (Score: 45/100)
   ✗ Code quality below threshold
   ✗ Found 15 critical issues
   ✗ Technical debt too high

3. Unit Tests ................................. FAILED (135/150)
   ✗ 15 tests failed
   ✗ Code coverage: 68% (below 80% threshold)

4. Integration Tests .......................... FAILED (42/50)
   ✗ 8 integration tests failed
   ✗ Regression detected in API endpoints
"""
            conclusion = "✗ VALIDATION FAILED - Release REJECTED"

        evidence_content = f"""
=================================================================
                 RELEASE VALIDATION EVIDENCE
=================================================================

Evidence ID: {evidence_id}
Version: {version}
Validation Date: {timestamp}
Overall Status: {'PASSED' if validation_passed else 'FAILED'}

-----------------------------------------------------------------
                    VALIDATION RESULTS
-----------------------------------------------------------------
{test_results}
-----------------------------------------------------------------
                      CONCLUSION
-----------------------------------------------------------------

{conclusion}

=================================================================
              This is an automated validation report
=================================================================
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
