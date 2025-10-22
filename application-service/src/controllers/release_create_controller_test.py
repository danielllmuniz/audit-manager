from datetime import datetime, timezone
from unittest import mock
import pytest
from src.models.mysql.entities.releases import ReleasesTable, EnvironmentEnum, StatusEnum
from src.models.mysql.entities.applications import ApplicationsTable
from src.errors.error_types.http_not_found import HttpNotFoundError
from src.errors.error_types.http_unprocessable_entity import HttpUnprocessableEntityError
from .release_create_controller import ReleaseCreatorController


class MockReleaseRepository:
    def __init__(self):
        self.created_release = None

    def create_release(self, application_id: int, version: str, env: EnvironmentEnum, evidence_url: str, status: StatusEnum):
        mock_app = ApplicationsTable(id=application_id, name="TestApp", owner_team="TeamA", repo_url="http://repo1")

        self.created_release = ReleasesTable(
            id=1,
            application_id=application_id,
            version=version,
            env=env,
            status=status,
            evidence_url=evidence_url,
            created_at=datetime.now(timezone.utc),
            application=mock_app
        )
        return self.created_release


class MockApplicationRepository:
    def __init__(self, application=None):
        self.application = application

    def get_application(self, application_id: int):
        _ = application_id
        return self.application


def test_create_release_validation_passed():
    mock_app = ApplicationsTable(
        id=1,
        name="TestApp",
        owner_team="TeamA",
        repo_url="http://github.com/TestApp",
        created_at=datetime.now(timezone.utc)
    )

    controller = ReleaseCreatorController(
        MockReleaseRepository(),
        MockApplicationRepository(mock_app)
    )

    with mock.patch.object(controller, '_ReleaseCreatorController__simulate_validation', return_value=(True, "/evidences/test.txt")):
        response = controller.create({
            "application_id": 1,
            "version": "1.0.0",
            "env": "DEV"
        })

    assert "data" in response
    assert response["data"]["version"] == "1.0.0"
    assert response["data"]["status"] == "PENDING_PREPROD"  # Passed validation
    assert response["data"]["application_name"] == "TestApp"


def test_create_release_validation_failed():
    mock_app = ApplicationsTable(
        id=1,
        name="TestApp",
        owner_team="TeamA",
        repo_url="http://github.com/TestApp",
        created_at=datetime.now(timezone.utc)
    )

    controller = ReleaseCreatorController(
        MockReleaseRepository(),
        MockApplicationRepository(mock_app)
    )

    # Mock the simulate_validation method to always return passed=False
    with mock.patch.object(controller, '_ReleaseCreatorController__simulate_validation', return_value=(False, "/evidences/test.txt")):
        response = controller.create({
            "application_id": 1,
            "version": "1.0.0",
            "env": "DEV"
        })

    assert "data" in response
    assert response["data"]["version"] == "1.0.0"
    assert response["data"]["status"] == "REJECTED"
    assert response["data"]["application_name"] == "TestApp"


def test_create_release_default_env():
    """Test creating a release without specifying environment (should default to DEV)"""
    mock_app = ApplicationsTable(
        id=1,
        name="TestApp",
        owner_team="TeamA",
        repo_url="http://github.com/TestApp",
        created_at=datetime.now(timezone.utc)
    )

    controller = ReleaseCreatorController(
        MockReleaseRepository(),
        MockApplicationRepository(mock_app)
    )

    with mock.patch.object(controller, '_ReleaseCreatorController__simulate_validation', return_value=(True, "/evidences/test.txt")):
        response = controller.create({
            "application_id": 1,
            "version": "1.0.0"
            # env not specified
        })

    assert "data" in response
    assert response["data"]["env"] == "DEV"


def test_create_release_invalid_environment():
    """Test creating a release with invalid environment"""
    mock_app = ApplicationsTable(
        id=1,
        name="TestApp",
        owner_team="TeamA",
        repo_url="http://github.com/TestApp",
        created_at=datetime.now(timezone.utc)
    )

    controller = ReleaseCreatorController(
        MockReleaseRepository(),
        MockApplicationRepository(mock_app)
    )

    with pytest.raises(HttpUnprocessableEntityError):
        controller.create({
            "application_id": 1,
            "version": "1.0.0",
            "env": "INVALID_ENV"
        })


def test_create_release_application_not_found():
    controller = ReleaseCreatorController(
        MockReleaseRepository(),
        MockApplicationRepository(None)  # Application not found
    )

    with pytest.raises(HttpNotFoundError):
        controller.create({
            "application_id": 999,
            "version": "1.0.0",
            "env": "DEV"
        })


def test_create_release_with_preprod_env():
    mock_app = ApplicationsTable(
        id=1,
        name="TestApp",
        owner_team="TeamA",
        repo_url="http://github.com/TestApp",
        created_at=datetime.now(timezone.utc)
    )

    controller = ReleaseCreatorController(
        MockReleaseRepository(),
        MockApplicationRepository(mock_app)
    )

    # Mock the simulate_validation method
    with mock.patch.object(controller, '_ReleaseCreatorController__simulate_validation', return_value=(True, "/evidences/test.txt")):
        response = controller.create({
            "application_id": 1,
            "version": "1.0.0",
            "env": "PREPROD"
        })

    assert "data" in response
    assert response["data"]["env"] == "PREPROD"
    assert response["data"]["version"] == "1.0.0"
