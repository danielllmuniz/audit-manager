from datetime import datetime, timezone
import pytest
from src.models.mysql.entities.releases import ReleasesTable, EnvironmentEnum, StatusEnum
from src.models.mysql.entities.applications import ApplicationsTable
from src.models.mysql.entities.approvals import ApprovalsTable, OutcomeEnum
from src.errors.error_types.http_not_found import HttpNotFoundError
from .release_get_controller import ReleaseGetController


class MockReleaseRepository:
    def __init__(self, release=None):
        self.release = release

    def get_release(self, release_id: int):
        _ = release_id
        return self.release


def test_get_release():
    mock_app = ApplicationsTable(id=1, name="App1", owner_team="TeamA", repo_url="http://repo1")

    mock_release = ReleasesTable(
        id=1,
        application_id=1,
        version="1.0.0",
        env=EnvironmentEnum.DEV,
        status=StatusEnum.CREATED,
        evidence_url="/evidences/test.txt",
        created_at=datetime.now(timezone.utc),
        deployed_at=None,
        deployed_preprod_at=None,
        deployed_prod_at=None,
        application=mock_app
    )
    mock_release.approvals = []

    controller = ReleaseGetController(MockReleaseRepository(mock_release))
    response = controller.get(1)

    assert "data" in response
    assert response["data"]["release_id"] == 1
    assert response["data"]["version"] == "1.0.0"
    assert response["data"]["application_name"] == "App1"
    assert "approvals" in response["data"]


def test_get_release_with_approvals():
    mock_app = ApplicationsTable(id=1, name="App1", owner_team="TeamA", repo_url="http://repo1")

    mock_approval = ApprovalsTable(
        id=1,
        release_id=1,
        approver_email="approver@test.com",
        outcome=OutcomeEnum.APPROVED,
        notes="Looks good",
        timestamp=datetime.now(timezone.utc)
    )

    mock_release = ReleasesTable(
        id=1,
        application_id=1,
        version="1.0.0",
        env=EnvironmentEnum.DEV,
        status=StatusEnum.APPROVED_PREPROD,
        evidence_url="/evidences/test.txt",
        created_at=datetime.now(timezone.utc),
        deployed_at=None,
        deployed_preprod_at=None,
        deployed_prod_at=None,
        application=mock_app
    )
    mock_release.approvals = [mock_approval]

    controller = ReleaseGetController(MockReleaseRepository(mock_release))
    response = controller.get(1)

    assert "data" in response
    assert len(response["data"]["approvals"]) == 1
    assert response["data"]["approvals"][0]["approver_email"] == "approver@test.com"
    assert response["data"]["approvals"][0]["outcome"] == "APPROVED"


def test_get_release_not_found():
    controller = ReleaseGetController(MockReleaseRepository(None))

    with pytest.raises(HttpNotFoundError):
        controller.get(999)
