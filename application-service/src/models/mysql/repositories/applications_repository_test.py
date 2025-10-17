from unittest import mock
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
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

def test_list_applications():
    mock_connection = MockConnection()
    repo = ApplicationsRepository(mock_connection)
    response = repo.list_applications()

    mock_connection.session.query.assert_called_once_with(ApplicationsTable)
    mock_connection.session.query().all.assert_called_once()
    mock_connection.session.query().filter.assert_not_called()

    assert len(response) == 3
    assert response[0].name == "App1"
