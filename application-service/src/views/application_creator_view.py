from src.controllers.interfaces.application_create_controller import ApplicationCreateController
from src.validators.application_creator_validator import application_creator_validator
from src.validators.dev_role_validator import dev_role_validator
from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse
from .interfaces.view_interface import ViewInterface

class ApplicationCreatorView(ViewInterface):
    def __init__(self, controller: ApplicationCreateController) -> None:
        self.__controller = controller
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        dev_role_validator(http_request)
        application_creator_validator(http_request)
        application_info = http_request.body
        body_response = self.__controller.create(application_info)

        return HttpResponse(status_code=201, body=body_response)
