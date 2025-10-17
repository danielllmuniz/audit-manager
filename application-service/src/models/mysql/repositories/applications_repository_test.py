from unittest import mock
import pytest
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from sqlalchemy.orm.exc import NoResultFound
from src.models.mysql.entities.applications import ApplicationsTable
from .applications_repository import ApplicationsRepository

class MockConnection:
    def __init__(self) -> None:
        self.session = UnifiedAlchemyMagicMock(
            data=[
                (
                    [mock.call.query(ApplicationsTable)],
                    [
                        ApplicationsTable(id=1, name="App1", owner_team="TeamA", repo_url="http://repo1", created_at=None),
                        ApplicationsTable(id=2, name="App2", owner_team="TeamB", repo_url="http://repo2", created_at=None),
                        ApplicationsTable(id=3, name="App3", owner_team="TeamC", repo_url="http://repo3", created_at=None),
                    ],
                )
            ]
        )
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): pass
class MockConnectionNoResult:
    def __init__(self) -> None:
        self.session = UnifiedAlchemyMagicMock()
        self.session.query.side_effect = self.__raise_no_result_found

    def __raise_no_result_found(self, *args, **kwargs):
        raise NoResultFound("No result found")

    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): pass


def test_list_applications():
    mock_connection = MockConnection()
    repo = ApplicationsRepository(mock_connection)
    response = repo.list_applications()

    mock_connection.session.query.assert_called_once_with(ApplicationsTable)
    mock_connection.session.query().all.assert_called_once()
    mock_connection.session.query().filter.assert_not_called()

    assert len(response) == 3
    assert response[0].name == "App1"

def test_list_applications_no_results():
    mock_connection = MockConnectionNoResult()
    repo = ApplicationsRepository(mock_connection)
    response = repo.list_applications()

    mock_connection.session.query.assert_called_once_with(ApplicationsTable)
    mock_connection.session.all.assert_not_called()
    mock_connection.session.filter.assert_not_called()

    assert len(response) == 0
    assert response == []

def test_delete_application():
    app_name = "App2"
    mock_connection = MockConnection()
    repo = ApplicationsRepository(mock_connection)
    repo.delete_application(app_name)

    mock_connection.session.query.assert_called_once_with(ApplicationsTable)
    mock_connection.session.query().filter.assert_called_once_with(ApplicationsTable.name == app_name)
    mock_connection.session.query().filter().delete.assert_called_once()
    mock_connection.session.commit.assert_called_once()
    mock_connection.session.rollback.assert_not_called()

def test_delete_application_error():
    mock_connection = MockConnectionNoResult()
    repo = ApplicationsRepository(mock_connection)

    with pytest.raises(Exception):
        repo.delete_application("app_name")

    mock_connection.session.rollback.assert_called_once()
