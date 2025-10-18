from typing import Dict
# import re
from src.models.mysql.interfaces.application_repository import ApplicationRepositoryInterface
from src.models.mysql.entities.applications import ApplicationsTable
from src.errors.error_types.http_unprocessable_entity import HttpUnprocessableEntityError
# from src.errors.error_types.http_bad_request import HttpBadRequestError
class ApplicationCreatorController:
    def __init__(self, application_repository: ApplicationRepositoryInterface) -> None:
        self.__application_repository = application_repository

    def create(self, person_info: Dict) -> Dict:
        name = person_info["name"]
        owner_team = person_info["owner_team"]
        repo_url = person_info["repo_url"]

        self.__validate_name_uniqueness(name)
        # self.__validate_input(name, owner_team)
        application_created = self.__insert_person_in_db(name, owner_team, repo_url)
        formated_response = self.__format_response(application_created)
        return formated_response



    def __validate_name_uniqueness(self, name: str) -> None:
        existing_application = self.__application_repository.get_application_by_name(name)
        if existing_application:
            raise HttpUnprocessableEntityError(f"Application with name '{name}' already exists")

    # def __validate_input(self, name: str, owner_team: str) -> None:
    #     non_valid_caracteres = re.compile(r'[^a-zA-Z]')
    #     if non_valid_caracteres.search(name):
    #         raise HttpBadRequestError("The name can only contain letters from A to Z")
    #     if non_valid_caracteres.search(owner_team):
    #         raise HttpBadRequestError("The owner_team can only contain letters from A to Z")

    def __insert_person_in_db(self, name: str, owner_team: str, repo_url: str) -> ApplicationsTable:
        application_created = self.__application_repository.create_application(name, owner_team, repo_url)
        return application_created

    def __format_response(self, application_created: ApplicationsTable) -> Dict:
        response = {
            "data" : {
                    "application_id": application_created.id,
                    "name": application_created.name,
                    "owner_team": application_created.owner_team,
                    "repo_url": application_created.repo_url
                }
        }
        return response
