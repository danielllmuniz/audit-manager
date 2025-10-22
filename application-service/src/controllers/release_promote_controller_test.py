from datetime import datetime, timezone
from unittest import mock
import pytest
from src.models.mysql.entities.releases import ReleasesTable, EnvironmentEnum, StatusEnum
from src.models.mysql.entities.applications import ApplicationsTable
from src.errors.error_types.http_not_found import HttpNotFoundError
from src.errors.error_types.http_unprocessable_entity import HttpUnprocessableEntityError
from src.errors.error_types.http_bad_request import HttpBadRequestError
from .release_promote_controller import ReleasePromoterController


class MockReleaseRepository:
    def __init__(self, release=None, updated_release=None):
        self.release = release
        self.updated_release = updated_release or release

    def get_release(self, release_id: int):
        _ = release_id
        return self.release

    def update_release(self, release_id: int, update_data: dict):
        _ = release_id
        if self.updated_release:
            for key, value in update_data.items():
                setattr(self.updated_release, key, value)
        return self.updated_release


def test_promote_release_approved_preprod():
    """Test promoting a release with APPROVED_PREPROD status"""
    mock_app = ApplicationsTable(id=1, name="App1", owner_team="TeamA", repo_url="http://repo1")

    mock_release = ReleasesTable(
        id=1,
        application_id=1,
        version="1.0.0",
        env=EnvironmentEnum.DEV,
        status=StatusEnum.APPROVED_PREPROD,
        evidence_url="/evidences/test.txt",
        created_at=datetime.now(timezone.utc),
        deployed_preprod_at=None,
        deployed_prod_at=None,
        application=mock_app
    )

    controller = ReleasePromoterController(MockReleaseRepository(mock_release))

    # Mock the fake_deployment method to always return success
    with mock.patch.object(controller, '_ReleasePromoterController__fake_deployment', return_value=(True, "Deployment successful")):
        response = controller.promote(release_id=1, user_role="DEVOPS")

    assert "data" in response
    # Should be promoted to PREPROD with PENDING_PROD status after successful deployment
    assert response["data"]["status"] == "PENDING_PROD"
    assert response["data"]["env"] == "PREPROD"


def test_promote_release_approved_prod():
    """Test promoting a release with APPROVED_PROD status"""
    mock_app = ApplicationsTable(id=1, name="App1", owner_team="TeamA", repo_url="http://repo1")

    mock_release = ReleasesTable(
        id=1,
        application_id=1,
        version="1.0.0",
        env=EnvironmentEnum.PREPROD,
        status=StatusEnum.APPROVED_PROD,
        evidence_url="/evidences/test.txt",
        created_at=datetime.now(timezone.utc),
        deployed_preprod_at=datetime.now(timezone.utc),
        deployed_prod_at=None,
        application=mock_app
    )

    controller = ReleasePromoterController(MockReleaseRepository(mock_release))

    # Mock the fake_deployment method to always return success
    with mock.patch.object(controller, '_ReleasePromoterController__fake_deployment', return_value=(True, "Deployment successful")):
        response = controller.promote(release_id=1, user_role="DEVOPS")

    assert "data" in response
    # Should be promoted to PROD with DEPLOYED status after successful deployment
    assert response["data"]["status"] == "DEPLOYED"
    assert response["data"]["env"] == "PROD"


def test_promote_release_deployment_failure():
    """Test promoting a release when deployment fails"""
    mock_app = ApplicationsTable(id=1, name="App1", owner_team="TeamA", repo_url="http://repo1")

    mock_release = ReleasesTable(
        id=1,
        application_id=1,
        version="1.0.0",
        env=EnvironmentEnum.DEV,
        status=StatusEnum.APPROVED_PREPROD,
        evidence_url="/evidences/test.txt",
        created_at=datetime.now(timezone.utc),
        deployed_preprod_at=None,
        deployed_prod_at=None,
        application=mock_app
    )

    controller = ReleasePromoterController(MockReleaseRepository(mock_release))

    # Mock the fake_deployment method to always return failure
    with mock.patch.object(controller, '_ReleasePromoterController__fake_deployment', return_value=(False, "Deployment failed")):
        response = controller.promote(release_id=1, user_role="DEVOPS")

    assert "data" in response
    # Should be marked as REJECTED after failed deployment
    assert response["data"]["status"] == "REJECTED"


def test_promote_release_invalid_role():
    """Test promoting a release with invalid user role"""
    mock_app = ApplicationsTable(id=1, name="App1", owner_team="TeamA", repo_url="http://repo1")

    mock_release = ReleasesTable(
        id=1,
        application_id=1,
        version="1.0.0",
        env=EnvironmentEnum.DEV,
        status=StatusEnum.APPROVED_PREPROD,
        evidence_url="/evidences/test.txt",
        created_at=datetime.now(timezone.utc),
        application=mock_app
    )

    controller = ReleasePromoterController(MockReleaseRepository(mock_release))

    with pytest.raises(HttpBadRequestError):
        controller.promote(release_id=1, user_role="DEVELOPER")


def test_promote_release_invalid_status():
    """Test promoting a release with invalid status"""
    mock_app = ApplicationsTable(id=1, name="App1", owner_team="TeamA", repo_url="http://repo1")

    mock_release = ReleasesTable(
        id=1,
        application_id=1,
        version="1.0.0",
        env=EnvironmentEnum.DEV,
        status=StatusEnum.CREATED,  # Invalid status for promotion
        evidence_url="/evidences/test.txt",
        created_at=datetime.now(timezone.utc),
        application=mock_app
    )

    controller = ReleasePromoterController(MockReleaseRepository(mock_release))

    with pytest.raises(HttpUnprocessableEntityError):
        controller.promote(release_id=1, user_role="DEVOPS")


def test_promote_release_not_found():
    """Test promoting a release that doesn't exist"""
    controller = ReleasePromoterController(MockReleaseRepository(None))

    with pytest.raises(HttpNotFoundError):
        controller.promote(release_id=999, user_role="DEVOPS")
