from src.controllers.interfaces.release_list_controller import ReleaseListController
from src.validators.list_role_validator import list_role_validator
from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse
from .interfaces.view_interface import ViewInterface

class ReleaseListerView(ViewInterface):
    def __init__(self, controller: ReleaseListController) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        list_role_validator(http_request)

        query_params = http_request.query or {}
        application_id = query_params.get('applicationId')

        if application_id:
            try:
                application_id = int(application_id)
            except (ValueError, TypeError):
                application_id = None

        body_response = self.__controller.list(application_id=application_id)
        return HttpResponse(status_code=200, body=body_response)
