from src.models.mysql.settings.connection import db_connection_handler
from src.models.mysql.repositories.applications_repository import ApplicationsRepository
from src.controllers.application_list_controller import ApplicationListerController
from src.views.application_lister_view import ApplicationListerView

def application_lister_composer():
    model = ApplicationsRepository(db_connection_handler)
    controller = ApplicationListerController(model)
    view = ApplicationListerView(controller)
    return view
