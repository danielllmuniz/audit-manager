from typing import Dict
from src.models.mysql.interfaces.release_repository import ReleaseRepositoryInterface
from src.models.mysql.interfaces.application_repository import ApplicationRepositoryInterface
from src.models.mysql.entities.releases import ReleasesTable, EnvironmentEnum
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
        env = release_info["env"]
        evidence_url = release_info.get("evidence_url")

        self.__validate_application_exists(application_id)
        env_enum = self.__validate_and_convert_env(env)

        release_created = self.__insert_release_in_db(
            application_id,
            version,
            env_enum,
            evidence_url
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

    def __insert_release_in_db(
        self,
        application_id: int,
        version: str,
        env: EnvironmentEnum,
        evidence_url: str = None
    ) -> ReleasesTable:
        release_created = self.__release_repository.create_release(
            application_id,
            version,
            env,
            evidence_url
        )
        return release_created

    def __format_response(self, release_created: ReleasesTable) -> Dict:
        response = {
            "data": {
                "release_id": release_created.id,
                "application_id": release_created.application_id,
                "version": release_created.version,
                "env": release_created.env.value,
                "status": release_created.status.value,
                "evidence_url": release_created.evidence_url,
                "created_at": release_created.created_at.isoformat()
            }
        }
        return response
