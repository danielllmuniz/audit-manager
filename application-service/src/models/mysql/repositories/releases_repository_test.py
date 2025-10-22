from unittest import mock
from datetime import datetime, timezone
import pytest
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from sqlalchemy.orm.exc import NoResultFound
from src.models.mysql.entities.releases import ReleasesTable, EnvironmentEnum, StatusEnum
from src.models.mysql.entities.applications import ApplicationsTable
from .releases_repository import ReleasesRepository


class MockConnection:
    def __init__(self, release_data=None) -> None:
        if release_data is None:
            release_data = [
                ReleasesTable(
                    id=1,
                    application_id=1,
                    version="1.0.0",
                    env=EnvironmentEnum.DEV,
                    status=StatusEnum.CREATED,
                    evidence_url="/evidences/test1.txt",
                    created_at=datetime.now(timezone.utc),
                    application=ApplicationsTable(id=1, name="App1", owner_team="TeamA", repo_url="http://repo1")
                ),
                ReleasesTable(
                    id=2,
                    application_id=1,
                    version="1.1.0",
                    env=EnvironmentEnum.PREPROD,
                    status=StatusEnum.PENDING_PREPROD,
                    evidence_url="/evidences/test2.txt",
                    created_at=datetime.now(timezone.utc),
                    application=ApplicationsTable(id=1, name="App1", owner_team="TeamA", repo_url="http://repo1")
                ),
                ReleasesTable(
                    id=3,
                    application_id=2,
                    version="2.0.0",
                    env=EnvironmentEnum.PROD,
                    status=StatusEnum.DEPLOYED,
                    evidence_url="/evidences/test3.txt",
                    created_at=datetime.now(timezone.utc),
                    application=ApplicationsTable(id=2, name="App2", owner_team="TeamB", repo_url="http://repo2")
                ),
            ]

        self.session = UnifiedAlchemyMagicMock(
            data=[
                (
                    [mock.call.query(ReleasesTable)],
                    release_data,
                )
            ]
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class MockConnectionNoResult:
    def __init__(self) -> None:
        self.session = UnifiedAlchemyMagicMock()
        self.session.query.side_effect = self.__raise_no_result_found

    def __raise_no_result_found(self, *args, **kwargs):
        raise NoResultFound("No result found")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class MockConnectionError:
    def __init__(self) -> None:
        self.session = UnifiedAlchemyMagicMock()
        self.session.add.side_effect = Exception("Database error")
        self.session.commit.side_effect = Exception("Database error")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class MockConnectionCommitError:
    """Mock that allows queries to work but fails on commit"""
    def __init__(self) -> None:
        single_release = [
            ReleasesTable(
                id=1,
                application_id=1,
                version="1.0.0",
                env=EnvironmentEnum.DEV,
                status=StatusEnum.CREATED,
                evidence_url="/evidences/test.txt",
                created_at=datetime.now(timezone.utc),
                application=ApplicationsTable(id=1, name="App1", owner_team="TeamA", repo_url="http://repo1")
            )
        ]

        self.session = UnifiedAlchemyMagicMock(
            data=[
                (
                    [mock.call.query(ReleasesTable)],
                    single_release,
                )
            ]
        )
        self.session.commit.side_effect = Exception("Database commit error")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def test_create_release():
    """Test creating a release with manual mock setup"""

    class MockCreateConnection:
        def __init__(self):
            self.session = mock.MagicMock()

            release = ReleasesTable(
                id=1,
                application_id=1,
                version="1.0.0",
                env=EnvironmentEnum.DEV,
                status=StatusEnum.CREATED,
                evidence_url="/evidences/test.txt",
                created_at=datetime.now(timezone.utc),
                application=ApplicationsTable(id=1, name="App1", owner_team="TeamA", repo_url="http://repo1")
            )

            self.session.query.return_value.options.return_value.filter.return_value.one.return_value = release

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    mock_connection = MockCreateConnection()
    repo = ReleasesRepository(mock_connection)

    release = repo.create_release(
        application_id=1,
        version="1.0.0",
        env=EnvironmentEnum.DEV,
        evidence_url="/evidences/test.txt",
        status=StatusEnum.CREATED
    )

    mock_connection.session.add.assert_called_once()
    mock_connection.session.commit.assert_called_once()
    mock_connection.session.refresh.assert_called_once()
    mock_connection.session.rollback.assert_not_called()

    assert release is not None
    assert release.version == "1.0.0"


def test_create_release_error():
    mock_connection = MockConnectionError()
    repo = ReleasesRepository(mock_connection)

    with pytest.raises(Exception):
        repo.create_release(
            application_id=1,
            version="1.0.0",
            env=EnvironmentEnum.DEV,
            evidence_url="/evidences/test.txt",
            status=StatusEnum.CREATED
        )

    mock_connection.session.rollback.assert_called_once()


def test_get_release():
    single_release = [
        ReleasesTable(
            id=1,
            application_id=1,
            version="1.0.0",
            env=EnvironmentEnum.DEV,
            status=StatusEnum.CREATED,
            evidence_url="/evidences/test.txt",
            created_at=datetime.now(timezone.utc),
            application=ApplicationsTable(id=1, name="App1", owner_team="TeamA", repo_url="http://repo1")
        )
    ]

    mock_connection = MockConnection(release_data=single_release)
    repo = ReleasesRepository(mock_connection)

    release = repo.get_release(1)

    mock_connection.session.query.assert_called_with(ReleasesTable)

    assert release is not None
    assert release.id == 1
    assert release.version == "1.0.0"


def test_get_release_not_found():
    mock_connection = MockConnectionNoResult()
    repo = ReleasesRepository(mock_connection)

    release = repo.get_release(999)

    assert release is None
    mock_connection.session.query.assert_called_once_with(ReleasesTable)


def test_list_releases():
    mock_connection = MockConnection()
    repo = ReleasesRepository(mock_connection)

    releases = repo.list_releases()

    mock_connection.session.query.assert_called_with(ReleasesTable)
    mock_connection.session.query().options.assert_called_once()
    mock_connection.session.query().options().order_by.assert_called_once()
    mock_connection.session.query().options().order_by().all.assert_called_once()

    assert len(releases) == 3
    assert releases[0].version == "1.0.0"


def test_list_releases_no_results():
    mock_connection = MockConnectionNoResult()
    repo = ReleasesRepository(mock_connection)

    releases = repo.list_releases()

    assert releases == []
    mock_connection.session.query.assert_called_once_with(ReleasesTable)


def test_list_releases_by_application():
    app1_releases = [
        ReleasesTable(
            id=1,
            application_id=1,
            version="1.0.0",
            env=EnvironmentEnum.DEV,
            status=StatusEnum.CREATED,
            evidence_url="/evidences/test1.txt",
            created_at=datetime.now(timezone.utc),
            application=ApplicationsTable(id=1, name="App1", owner_team="TeamA", repo_url="http://repo1")
        ),
        ReleasesTable(
            id=2,
            application_id=1,
            version="1.1.0",
            env=EnvironmentEnum.PREPROD,
            status=StatusEnum.PENDING_PREPROD,
            evidence_url="/evidences/test2.txt",
            created_at=datetime.now(timezone.utc),
            application=ApplicationsTable(id=1, name="App1", owner_team="TeamA", repo_url="http://repo1")
        ),
    ]

    mock_connection = MockConnection(release_data=app1_releases)
    repo = ReleasesRepository(mock_connection)

    releases = repo.list_releases_by_application(1)

    mock_connection.session.query.assert_called_with(ReleasesTable)
    mock_connection.session.query().options.assert_called_once()
    mock_connection.session.query().options().filter.assert_called_once()

    assert len(releases) == 2
    assert all(r.application_id == 1 for r in releases)


def test_list_releases_by_application_no_results():
    mock_connection = MockConnectionNoResult()
    repo = ReleasesRepository(mock_connection)

    releases = repo.list_releases_by_application(999)

    assert releases == []
    mock_connection.session.query.assert_called_once_with(ReleasesTable)


def test_update_release():
    single_release = [
        ReleasesTable(
            id=1,
            application_id=1,
            version="1.0.0",
            env=EnvironmentEnum.DEV,
            status=StatusEnum.CREATED,
            evidence_url="/evidences/test.txt",
            created_at=datetime.now(timezone.utc),
            application=ApplicationsTable(id=1, name="App1", owner_team="TeamA", repo_url="http://repo1")
        )
    ]

    mock_connection = MockConnection(release_data=single_release)
    repo = ReleasesRepository(mock_connection)

    update_data = {
        "status": StatusEnum.APPROVED_PREPROD,
        "deployment_logs": "Deployment successful"
    }

    release = repo.update_release(1, update_data)

    mock_connection.session.commit.assert_called_once()
    mock_connection.session.rollback.assert_not_called()

    assert mock_connection.session.query.call_count >= 2  # one for update, one for reload

    assert release is not None


def test_update_release_not_found():
    mock_connection = MockConnectionNoResult()
    repo = ReleasesRepository(mock_connection)

    update_data = {"status": StatusEnum.APPROVED_PREPROD}
    release = repo.update_release(999, update_data)

    assert release is None
    mock_connection.session.query.assert_called_with(ReleasesTable)


def test_update_release_error():
    mock_connection = MockConnectionCommitError()
    repo = ReleasesRepository(mock_connection)

    update_data = {"status": StatusEnum.APPROVED_PREPROD}

    with pytest.raises(Exception):
        repo.update_release(1, update_data)

    mock_connection.session.rollback.assert_called_once()
