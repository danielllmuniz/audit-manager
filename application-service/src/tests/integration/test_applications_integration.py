import pytest
from src.models.mysql.repositories.applications_repository import ApplicationsRepository
from src.controllers.application_create_controller import ApplicationCreatorController
from src.controllers.application_list_controller import ApplicationListerController
from src.controllers.application_get_controller import ApplicationGetController
from src.errors.error_types.http_not_found import HttpNotFoundError
from src.errors.error_types.http_unprocessable_entity import HttpUnprocessableEntityError


class TestApplicationsRepositoryIntegration:
    def test_create_and_list_applications(self, db_connection):
        repo = ApplicationsRepository(db_connection)

        app = repo.create_application(
            name="TestApp",
            owner_team="TeamA",
            repo_url="http://github.com/TestApp"
        )

        assert app.id is not None
        assert app.name == "TestApp"
        assert app.owner_team == "TeamA"

        apps = repo.list_applications()
        assert len(apps) == 1
        assert apps[0].name == "TestApp"

    def test_get_application_by_id(self, db_connection):
        repo = ApplicationsRepository(db_connection)

        app = repo.create_application(
            name="TestApp",
            owner_team="TeamA",
            repo_url="http://github.com/TestApp"
        )

        retrieved_app = repo.get_application(app.id)
        assert retrieved_app is not None
        assert retrieved_app.id == app.id
        assert retrieved_app.name == "TestApp"

    def test_get_application_by_name(self, db_connection):
        repo = ApplicationsRepository(db_connection)

        repo.create_application(
            name="TestApp",
            owner_team="TeamA",
            repo_url="http://github.com/TestApp"
        )

        retrieved_app = repo.get_application_by_name("TestApp")
        assert retrieved_app is not None
        assert retrieved_app.name == "TestApp"

        non_existent = repo.get_application_by_name("NonExistent")
        assert non_existent is None



class TestApplicationsControllerIntegration:

    def test_create_application_controller(self, db_connection):
        repo = ApplicationsRepository(db_connection)
        controller = ApplicationCreatorController(repo)

        response = controller.create({
            "name": "TestApp",
            "owner_team": "TeamA",
            "repo_url": "http://github.com/TestApp"
        })

        assert "data" in response
        assert response["data"]["name"] == "TestApp"
        assert response["data"]["application_id"] is not None

        apps = repo.list_applications()
        assert len(apps) == 1

    def test_create_duplicate_application(self, db_connection):
        repo = ApplicationsRepository(db_connection)
        controller = ApplicationCreatorController(repo)

        controller.create({
            "name": "TestApp",
            "owner_team": "TeamA",
            "repo_url": "http://github.com/TestApp"
        })

        with pytest.raises(HttpUnprocessableEntityError):
            controller.create({
                "name": "TestApp",
                "owner_team": "TeamB",
                "repo_url": "http://github.com/TestApp2"
            })

    def test_list_applications_controller(self, db_connection):
        repo = ApplicationsRepository(db_connection)
        controller = ApplicationListerController(repo)

        repo.create_application("App1", "TeamA", "http://repo1")
        repo.create_application("App2", "TeamB", "http://repo2")

        response = controller.list()

        assert "data" in response
        assert len(response["data"]) == 2

    def test_get_application_controller(self, db_connection):
        repo = ApplicationsRepository(db_connection)
        controller = ApplicationGetController(repo)

        app = repo.create_application("TestApp", "TeamA", "http://repo1")

        response = controller.get(app.id)

        assert "data" in response
        assert response["data"]["name"] == "TestApp"

    def test_get_nonexistent_application(self, db_connection):
        repo = ApplicationsRepository(db_connection)
        controller = ApplicationGetController(repo)

        with pytest.raises(HttpNotFoundError):
            controller.get(999)
