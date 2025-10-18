from src.models.mysql.settings.connection import db_connection_handler
from src.models.mysql.repositories.releases_repository import ReleasesRepository
from src.controllers.release_approve_controller import ReleaseApproverController
from src.views.release_approver_view import ReleaseApproverView

def release_approver_composer():
    model = ReleasesRepository(db_connection_handler)
    controller = ReleaseApproverController(model)
    view = ReleaseApproverView(controller)
    return view
