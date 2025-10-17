import pytest
from src.models.mysql.settings.connection import db_connection_handler
from .applications_repository import ApplicationsRepository

# db_connection_handler.connect_to_db()

@pytest.mark.skip(reason="Requires a live database connection")
def test_list_applications():
    repo = ApplicationsRepository(db_connection_handler)
    response = repo.list_applications()
    print(response)

def test_delete_application():
    name = "non_existent_app"
    repo = ApplicationsRepository(db_connection_handler)
    repo.delete_application(name)
