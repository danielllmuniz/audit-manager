from src.models.mysql.settings.connection import db_connection_handler
from src.models.mysql.repositories.releases_repository import ReleasesRepository
from src.controllers.release_promote_controller import ReleasePromoterController
from src.views.release_promoter_view import ReleasePromoterView

def release_promoter_composer():
    model = ReleasesRepository(db_connection_handler)
    controller = ReleasePromoterController(model)
    view = ReleasePromoterView(controller)
    return view
