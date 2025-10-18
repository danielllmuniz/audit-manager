from src.models.mysql.settings.connection import db_connection_handler
from src.models.mysql.repositories.releases_repository import ReleasesRepository
from src.models.mysql.repositories.applications_repository import ApplicationsRepository
from src.controllers.release_create_controller import ReleaseCreatorController
from src.views.release_creator_view import ReleaseCreatorView

def release_creator_composer():
    release_model = ReleasesRepository(db_connection_handler)
    application_model = ApplicationsRepository(db_connection_handler)
    controller = ReleaseCreatorController(release_model, application_model)
    view = ReleaseCreatorView(controller)
    return view
