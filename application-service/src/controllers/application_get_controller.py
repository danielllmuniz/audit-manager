from typing import Dict
from src.models.mysql.interfaces.application_repository import ApplicationRepositoryInterface
from src.models.mysql.entities.applications import ApplicationsTable
from src.errors.error_types.http_not_found import HttpNotFoundError

class ApplicationGetController:
    def __init__(self, application_repository: ApplicationRepositoryInterface) -> None:
        self.__application_repository = application_repository

    def get(self, application_id: int) -> Dict:
        application = self.__get_application_from_db(application_id)
        formated_response = self.__format_response(application)
        return formated_response

    def __get_application_from_db(self, application_id: int) -> ApplicationsTable:
        application = self.__application_repository.get_application(application_id)
        if not application:
            raise HttpNotFoundError(f"Application with id '{application_id}' not found")
        return application

    def __format_response(self, application: ApplicationsTable) -> Dict:
        response = {
            "data": {
                "application_id": application.id,
                "name": application.name,
                "owner_team": application.owner_team,
                "repo_url": application.repo_url,
                "created_at": application.created_at.isoformat()
            }
        }
        return response
