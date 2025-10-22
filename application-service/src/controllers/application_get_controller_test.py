from datetime import datetime, timezone
import pytest
from src.models.mysql.entities.applications import ApplicationsTable
from src.models.mysql.entities.releases import ReleasesTable, EnvironmentEnum, StatusEnum
from src.errors.error_types.http_not_found import HttpNotFoundError
from .application_get_controller import ApplicationGetController


class MockApplicationRepository:
    def __init__(self, application=None):
        self.application = application

    def get_application(self):
        return self.application


def test_get_application():
    mock_app = ApplicationsTable(
        id=1,
        name="TestApp",
        owner_team="DevTeam",
        repo_url="http://github.com/TestApp",
        created_at=datetime.now(timezone.utc)
    )
    mock_app.releases = []

    controller = ApplicationGetController(MockApplicationRepository(mock_app))
    response = controller.get(1)

    assert "data" in response
    assert response["data"]["application_id"] == 1
    assert response["data"]["name"] == "TestApp"
    assert response["data"]["owner_team"] == "DevTeam"
    assert "releases" in response["data"]


def test_get_application_with_releases():
    mock_release = ReleasesTable(
        id=1,
        application_id=1,
        version="1.0.0",
        env=EnvironmentEnum.DEV,
        status=StatusEnum.CREATED,
        evidence_url="/evidences/test.txt",
        created_at=datetime.now(timezone.utc),
        deployed_at=None
    )

    mock_app = ApplicationsTable(
        id=1,
        name="TestApp",
        owner_team="DevTeam",
        repo_url="http://github.com/TestApp",
        created_at=datetime.now(timezone.utc)
    )
    mock_app.releases = [mock_release]

    controller = ApplicationGetController(MockApplicationRepository(mock_app))
    response = controller.get(1)

    assert "data" in response
    assert len(response["data"]["releases"]) == 1
    assert response["data"]["releases"][0]["version"] == "1.0.0"


def test_get_application_not_found():
    controller = ApplicationGetController(MockApplicationRepository(None))

    with pytest.raises(HttpNotFoundError):
        controller.get(999)
