from typing import Dict, List
from src.models.mysql.interfaces.application_repository import ApplicationRepositoryInterface
from src.models.mysql.entities.applications import ApplicationsTable

class ApplicationListerController:
    def __init__(self, application_repository: ApplicationRepositoryInterface) -> None:
        self.__application_repository = application_repository

    def list(self) -> Dict:
        applications = self.__get_applications_from_db()
        formated_response = self.__format_response(applications)
        return formated_response

    def __get_applications_from_db(self) -> List[ApplicationsTable]:
        applications = self.__application_repository.list_applications()
        return applications

    def __format_response(self, applications: List[ApplicationsTable]) -> Dict:
        response = {
            "data": [
                {
                    "application_id": app.id,
                    "name": app.name,
                    "owner_team": app.owner_team,
                    "repo_url": app.repo_url,
                    "created_at": app.created_at.isoformat()
                }
                for app in applications
            ]
        }
        return response
