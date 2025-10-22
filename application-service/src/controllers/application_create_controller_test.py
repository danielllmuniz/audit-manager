import pytest
from src.models.mysql.entities.applications import ApplicationsTable
from .application_create_controller import ApplicationCreatorController

class MockApplicationRepository:
    def insert_application(self):
        pass

    def get_application_by_name(self):
        return None

    def create_application(self, name: str, owner_team: str, repo_url: str):
        app = ApplicationsTable(
            id=1,
            name=name,
            owner_team=owner_team,
            repo_url=repo_url
        )
        return app

def test_create():
    application_infos = {
        "name": "TestApp",
        "owner_team": "DevTeam",
        "repo_url": "http://github.com/TestApp"
    }

    controller = ApplicationCreatorController(MockApplicationRepository())
    response = controller.create(application_infos)

    assert response["data"]["name"] == "TestApp"
    assert response["data"]["owner_team"] == "DevTeam"
    assert response["data"]["repo_url"] == "http://github.com/TestApp"

def test_create_error():

    class MockApplicationRepositoryWithExisting:
        def get_application_by_name(self, name: str):
            if name == "ExistingApp":
                return ApplicationsTable(
                    id=1,
                    name=name,
                    owner_team="ExistingTeam",
                    repo_url="http://github.com/ExistingApp"
                )
            return None

        def create_application(self, name: str, owner_team: str, repo_url: str):
            app = ApplicationsTable(
                id=2,
                name=name,
                owner_team=owner_team,
                repo_url=repo_url
            )
            return app

    application_infos = {
        "name": "ExistingApp",
        "owner_team": "DevTeam",
        "repo_url": "http://github.com/TestApp"
    }

    controller = ApplicationCreatorController(MockApplicationRepositoryWithExisting())
    with pytest.raises(Exception):
        controller.create(application_infos)
