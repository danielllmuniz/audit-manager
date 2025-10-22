from datetime import datetime, timezone
import pytest
from src.models.mysql.entities.releases import ReleasesTable, EnvironmentEnum, StatusEnum
from src.models.mysql.entities.applications import ApplicationsTable
from src.models.mysql.entities.approvals import ApprovalsTable, OutcomeEnum
from src.errors.error_types.http_not_found import HttpNotFoundError
from src.errors.error_types.http_unprocessable_entity import HttpUnprocessableEntityError
from src.errors.error_types.http_bad_request import HttpBadRequestError
from .release_disapprove_controller import ReleaseDisapproverController


class MockReleaseRepository:
    def __init__(self, release=None, updated_release=None):
        self.release = release
        self.updated_release = updated_release or release

    def get_release(self, release_id: int = None):
        _ = release_id
        return self.release

    def update_release(self, release_id: int = None, update_data: dict = None):
        _ = release_id
        if self.updated_release and update_data:
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


def test_disapprove_release_pending_preprod():
    """Test disapproving a release with PENDING_PREPROD status"""
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

    controller = ReleaseDisapproverController(
        MockReleaseRepository(mock_release),
        MockApprovalRepository()
    )

    response = controller.disapprove(release_id=1, user_role="APPROVER", user_email="approver@test.com")

    assert "data" in response
    assert response["data"]["status"] == "REJECTED"


def test_disapprove_release_pending_prod():
    """Test disapproving a release with PENDING_PROD status"""
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

    controller = ReleaseDisapproverController(
        MockReleaseRepository(mock_release),
        MockApprovalRepository()
    )

    response = controller.disapprove(release_id=1, user_role="APPROVER", user_email="approver@test.com")

    assert "data" in response
    assert response["data"]["status"] == "REJECTED"


def test_disapprove_release_invalid_role():
    """Test disapproving a release with invalid user role"""
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

    controller = ReleaseDisapproverController(
        MockReleaseRepository(mock_release),
        MockApprovalRepository()
    )

    with pytest.raises(HttpBadRequestError):
        controller.disapprove(release_id=1, user_role="DEVELOPER", user_email="dev@test.com")


def test_disapprove_release_invalid_status():
    """Test disapproving a release with invalid status"""
    mock_app = ApplicationsTable(id=1, name="App1", owner_team="TeamA", repo_url="http://repo1")

    mock_release = ReleasesTable(
        id=1,
        application_id=1,
        version="1.0.0",
        env=EnvironmentEnum.DEV,
        status=StatusEnum.DEPLOYED,  # Invalid status for disapproval
        evidence_url="/evidences/test.txt",
        created_at=datetime.now(timezone.utc),
        application=mock_app
    )

    controller = ReleaseDisapproverController(
        MockReleaseRepository(mock_release),
        MockApprovalRepository()
    )

    with pytest.raises(HttpUnprocessableEntityError):
        controller.disapprove(release_id=1, user_role="APPROVER", user_email="approver@test.com")


def test_disapprove_release_not_found():
    """Test disapproving a release that doesn't exist"""
    controller = ReleaseDisapproverController(
        MockReleaseRepository(None),
        MockApprovalRepository()
    )

    with pytest.raises(HttpNotFoundError):
        controller.disapprove(release_id=999, user_role="APPROVER", user_email="approver@test.com")
