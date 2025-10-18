import pytest
from .application_create_controller import ApplicationCreatorController

class MockApplicationRepository:
    def insert_application(self, name: str, owner_team: str, repo_url: str):
        pass

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
    application_infos = {
        "name": "TestApp",
        "owner_team": "Dev Team!",
        "repo_url": "http://github.com/TestApp"
    }

    controller = ApplicationCreatorController(MockApplicationRepository())
    with pytest.raises(Exception):
        controller.create(application_infos)
