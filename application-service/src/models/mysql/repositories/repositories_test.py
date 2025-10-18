import pytest
from src.models.mysql.settings.connection import db_connection_handler
from .applications_repository import ApplicationsRepository

db_connection_handler.connect_to_db()

@pytest.mark.skip(reason="Requires a live database connection")
def test_list_applications():
    repo = ApplicationsRepository(db_connection_handler)
    response = repo.list_applications()
    print(response)

@pytest.mark.skip(reason="Requires a live database connection")
def test_delete_application():
    name = "non_existent_app"
    repo = ApplicationsRepository(db_connection_handler)
    repo.delete_application(name)

@pytest.mark.skip(reason="Requires a live database connection")
def test_create_application():
    name = "test_app"
    owner_team = "test_team"
    repo_url = "http://example.com/repo.git"
    repo = ApplicationsRepository(db_connection_handler)
    response = repo.create_application(name, owner_team, repo_url)
    print(response)

@pytest.mark.skip(reason="Requires a live database connection")
def test_get_application():
    application_id = 1
    repo = ApplicationsRepository(db_connection_handler)
    response = repo.get_application(application_id)
    print(response)
