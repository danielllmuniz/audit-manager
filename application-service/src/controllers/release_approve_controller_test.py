from datetime import datetime, timezone
import pytest
from src.models.mysql.entities.releases import ReleasesTable, EnvironmentEnum, StatusEnum
from src.models.mysql.entities.applications import ApplicationsTable
from src.models.mysql.entities.approvals import ApprovalsTable, OutcomeEnum
from src.errors.error_types.http_not_found import HttpNotFoundError
from src.errors.error_types.http_unprocessable_entity import HttpUnprocessableEntityError
from src.errors.error_types.http_bad_request import HttpBadRequestError
from .release_approve_controller import ReleaseApproverController


class MockReleaseRepository:
    def __init__(self, release=None, updated_release=None):
        self.release = release
        self.updated_release = updated_release or release

    def get_release(self):
        return self.release

    def update_release(self, update_data: dict):
        if self.updated_release:
            for key, value in update_data.items():
                setattr(self.updated_release, key, value)
        return self.updated_release


class MockApprovalRepository:
    def __init__(self):
        self.created_approval = None

    def create_approval(self, release_id: int, approver_email: str, outcome: OutcomeEnum, notes: str = None):
        self.created_approval = ApprovalsTable(
            id=1,
            release_id=release_id,
            approver_email=approver_email,
            outcome=outcome,
            notes=notes,
            timestamp=datetime.now(timezone.utc)
        )
        return self.created_approval


def test_approve_release_pending_preprod():
    mock_app = ApplicationsTable(id=1, name="App1", owner_team="TeamA", repo_url="http://repo1")

    mock_release = ReleasesTable(
        id=1,
        application_id=1,
        version="1.0.0",
        env=EnvironmentEnum.DEV,
        status=StatusEnum.PENDING_PREPROD,
        evidence_url="/evidences/test.txt",
        created_at=datetime.now(timezone.utc),
        application=mock_app
    )

    controller = ReleaseApproverController(
        MockReleaseRepository(mock_release),
        MockApprovalRepository()
    )

    response = controller.approve(release_id=1, user_role="APPROVER", user_email="approver@test.com")

    assert "data" in response
    assert response["data"]["status"] == "APPROVED_PREPROD"


def test_approve_release_pending_prod():
    mock_app = ApplicationsTable(id=1, name="App1", owner_team="TeamA", repo_url="http://repo1")

    mock_release = ReleasesTable(
        id=1,
        application_id=1,
        version="1.0.0",
        env=EnvironmentEnum.PREPROD,
        status=StatusEnum.PENDING_PROD,
        evidence_url="/evidences/test.txt",
        created_at=datetime.now(timezone.utc),
        application=mock_app
    )

    controller = ReleaseApproverController(
        MockReleaseRepository(mock_release),
        MockApprovalRepository()
    )

    response = controller.approve(release_id=1, user_role="APPROVER", user_email="approver@test.com")

    assert "data" in response
    assert response["data"]["status"] == "APPROVED_PROD"


def test_approve_release_invalid_role():
    mock_app = ApplicationsTable(id=1, name="App1", owner_team="TeamA", repo_url="http://repo1")

    mock_release = ReleasesTable(
        id=1,
        application_id=1,
        version="1.0.0",
        env=EnvironmentEnum.DEV,
        status=StatusEnum.PENDING_PREPROD,
        evidence_url="/evidences/test.txt",
        created_at=datetime.now(timezone.utc),
        application=mock_app
    )

    controller = ReleaseApproverController(
        MockReleaseRepository(mock_release),
        MockApprovalRepository()
    )

    with pytest.raises(HttpBadRequestError):
        controller.approve(release_id=1, user_role="DEVELOPER", user_email="dev@test.com")


def test_approve_release_invalid_status():
    mock_app = ApplicationsTable(id=1, name="App1", owner_team="TeamA", repo_url="http://repo1")

    mock_release = ReleasesTable(
        id=1,
        application_id=1,
        version="1.0.0",
        env=EnvironmentEnum.DEV,
        status=StatusEnum.CREATED,  # Invalid status for approval
        evidence_url="/evidences/test.txt",
        created_at=datetime.now(timezone.utc),
        application=mock_app
    )

    controller = ReleaseApproverController(
        MockReleaseRepository(mock_release),
        MockApprovalRepository()
    )

    with pytest.raises(HttpUnprocessableEntityError):
        controller.approve(release_id=1, user_role="APPROVER", user_email="approver@test.com")


def test_approve_release_not_found():
    controller = ReleaseApproverController(
        MockReleaseRepository(None),
        MockApprovalRepository()
    )

    with pytest.raises(HttpNotFoundError):
        controller.approve(release_id=999, user_role="APPROVER", user_email="approver@test.com")
