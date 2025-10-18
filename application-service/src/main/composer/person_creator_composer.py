
from src.models.mysql.settings.connection import db_connection_handler
from src.models.mysql.repositories.applications_repository import ApplicationsRepository
from src.controllers.application_create_controller import ApplicationCreatorController
from src.views.application_creator_view import ApplicationCreatorView

def person_creator_composer():
    model = ApplicationsRepository(db_connection_handler)
    controller = ApplicationCreatorController(model)
    view = ApplicationCreatorView(controller)
    return view
