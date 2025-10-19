from src.models.mysql.settings.connection import db_connection_handler
from src.models.mysql.repositories.releases_repository import ReleasesRepository
from src.models.mysql.repositories.approvals_repository import ApprovalsRepository
from src.controllers.release_approve_controller import ReleaseApproverController
from src.views.release_approver_view import ReleaseApproverView

def release_approver_composer():
    release_model = ReleasesRepository(db_connection_handler)
    approval_model = ApprovalsRepository(db_connection_handler)
    controller = ReleaseApproverController(release_model, approval_model)
    view = ReleaseApproverView(controller)
    return view
