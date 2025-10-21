from src.models.mysql.settings.connection import db_connection_handler
from src.models.mysql.repositories.applications_repository import ApplicationsRepository
from src.controllers.application_get_controller import ApplicationGetController
from src.views.application_get_view import ApplicationGetView

def application_get_composer():
    repository = ApplicationsRepository(db_connection_handler)
    controller = ApplicationGetController(repository)
    view = ApplicationGetView(controller)

    return view
