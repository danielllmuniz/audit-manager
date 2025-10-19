from src.models.mysql.settings.connection import db_connection_handler
from src.models.mysql.repositories.releases_repository import ReleasesRepository
from src.models.mysql.repositories.approvals_repository import ApprovalsRepository
from src.controllers.release_disapprove_controller import ReleaseDisapproverController
from src.views.release_disapprover_view import ReleaseDisapproverView

def release_disapprover_composer():
    release_model = ReleasesRepository(db_connection_handler)
    approval_model = ApprovalsRepository(db_connection_handler)
    controller = ReleaseDisapproverController(release_model, approval_model)
    view = ReleaseDisapproverView(controller)
    return view
