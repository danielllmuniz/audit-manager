from src.models.mysql.settings.connection import db_connection_handler
from src.models.mysql.repositories.releases_repository import ReleasesRepository
from src.controllers.release_list_controller import ReleaseListerController
from src.views.release_lister_view import ReleaseListerView

def release_lister_composer():
    model = ReleasesRepository(db_connection_handler)
    controller = ReleaseListerController(model)
    view = ReleaseListerView(controller)
    return view
