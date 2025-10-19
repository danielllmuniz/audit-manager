from src.controllers.interfaces.release_disapprove_controller import ReleaseDisapproveController
from src.validators.release_approve_validator import release_approve_validator
from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse
from .interfaces.view_interface import ViewInterface

class ReleaseDisapproverView(ViewInterface):
    def __init__(self, controller: ReleaseDisapproveController) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        user_role, user_email = release_approve_validator(http_request)
        release_id = http_request.param.get("release_id")
        body_response = self.__controller.disapprove(release_id, user_role, user_email)

        return HttpResponse(status_code=200, body=body_response)
