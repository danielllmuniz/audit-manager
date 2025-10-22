from datetime import datetime, timezone
from src.models.mysql.entities.applications import ApplicationsTable
from .application_list_controller import ApplicationListerController


class MockApplicationRepository:
    def __init__(self, applications=None):
        self.applications = applications or []

    def list_applications(self):
        return self.applications


def test_list_applications():
    mock_apps = [
        ApplicationsTable(
            id=1,
            name="App1",
            owner_team="TeamA",
            repo_url="http://github.com/App1",
            created_at=datetime.now(timezone.utc)
        ),
        ApplicationsTable(
            id=2,
            name="App2",
            owner_team="TeamB",
            repo_url="http://github.com/App2",
            created_at=datetime.now(timezone.utc)
        )
    ]

    controller = ApplicationListerController(MockApplicationRepository(mock_apps))
    response = controller.list()

    assert "data" in response
    assert len(response["data"]) == 2
    assert response["data"][0]["name"] == "App1"
    assert response["data"][0]["owner_team"] == "TeamA"
    assert response["data"][1]["name"] == "App2"


def test_list_applications_empty():
    controller = ApplicationListerController(MockApplicationRepository([]))
    response = controller.list()

    assert "data" in response
    assert len(response["data"]) == 0
    assert response["data"] == []
