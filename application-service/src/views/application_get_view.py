from src.controllers.interfaces.application_get_controller import ApplicationGetController
from src.validators.list_role_validator import list_role_validator
from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse
from .interfaces.view_interface import ViewInterface

class ApplicationGetView(ViewInterface):
    def __init__(self, controller: ApplicationGetController) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        list_role_validator(http_request)
        application_id = http_request.param["application_id"]
        body_response = self.__controller.get(application_id)
        return HttpResponse(status_code=200, body=body_response)
