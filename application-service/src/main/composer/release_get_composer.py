from src.models.mysql.settings.connection import db_connection_handler
from src.models.mysql.repositories.releases_repository import ReleasesRepository
from src.controllers.release_get_controller import ReleaseGetController
from src.views.release_get_view import ReleaseGetView


def release_get_composer():
    release_model = ReleasesRepository(db_connection_handler)
    controller = ReleaseGetController(release_model)
    view = ReleaseGetView(controller)
    return view
