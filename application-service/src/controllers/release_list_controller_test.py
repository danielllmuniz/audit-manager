from datetime import datetime, timezone
from src.models.mysql.entities.releases import ReleasesTable, EnvironmentEnum, StatusEnum
from src.models.mysql.entities.applications import ApplicationsTable
from .release_list_controller import ReleaseListerController


class MockReleaseRepository:
    def __init__(self, releases=None):
        self.releases = releases or []

    def list_releases(self):
        return self.releases

    def list_releases_by_application(self, application_id: int):
        return [r for r in self.releases if r.application_id == application_id]


def test_list_all_releases():
    mock_app = ApplicationsTable(id=1, name="App1", owner_team="TeamA", repo_url="http://repo1")

    mock_releases = [
        ReleasesTable(
            id=1,
            application_id=1,
            version="1.0.0",
            env=EnvironmentEnum.DEV,
            status=StatusEnum.CREATED,
            evidence_url="/evidences/test1.txt",
            created_at=datetime.now(timezone.utc),
            deployed_at=None,
            application=mock_app
        ),
        ReleasesTable(
            id=2,
            application_id=1,
            version="1.1.0",
            env=EnvironmentEnum.PREPROD,
            status=StatusEnum.PENDING_PREPROD,
            evidence_url="/evidences/test2.txt",
            created_at=datetime.now(timezone.utc),
            deployed_at=None,
            application=mock_app
        )
    ]

    controller = ReleaseListerController(MockReleaseRepository(mock_releases))
    response = controller.list()

    assert "data" in response
    assert len(response["data"]) == 2
    assert response["data"][0]["version"] == "1.0.0"
    assert response["data"][1]["version"] == "1.1.0"


def test_list_releases_by_application():
    mock_app1 = ApplicationsTable(id=1, name="App1", owner_team="TeamA", repo_url="http://repo1")
    mock_app2 = ApplicationsTable(id=2, name="App2", owner_team="TeamB", repo_url="http://repo2")

    mock_releases = [
        ReleasesTable(
            id=1,
            application_id=1,
            version="1.0.0",
            env=EnvironmentEnum.DEV,
            status=StatusEnum.CREATED,
            evidence_url="/evidences/test1.txt",
            created_at=datetime.now(timezone.utc),
            application=mock_app1
        ),
        ReleasesTable(
            id=2,
            application_id=2,
            version="2.0.0",
            env=EnvironmentEnum.DEV,
            status=StatusEnum.CREATED,
            evidence_url="/evidences/test2.txt",
            created_at=datetime.now(timezone.utc),
            application=mock_app2
        )
    ]

    controller = ReleaseListerController(MockReleaseRepository(mock_releases))
    response = controller.list(application_id=1)

    assert "data" in response
    assert len(response["data"]) == 1
    assert response["data"][0]["application_id"] == 1
    assert response["data"][0]["version"] == "1.0.0"


def test_list_releases_empty():
    controller = ReleaseListerController(MockReleaseRepository([]))
    response = controller.list()

    assert "data" in response
    assert len(response["data"]) == 0
    assert response["data"] == []
