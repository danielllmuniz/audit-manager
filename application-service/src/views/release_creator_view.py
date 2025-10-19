from src.controllers.interfaces.release_create_controller import ReleaseCreateController
from src.validators.release_creator_validator import release_creator_validator
from src.validators.dev_role_validator import dev_role_validator
from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse
from .interfaces.view_interface import ViewInterface

class ReleaseCreatorView(ViewInterface):
    def __init__(self, controller: ReleaseCreateController) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        dev_role_validator(http_request)
        release_creator_validator(http_request)
        release_info = http_request.body
        body_response = self.__controller.create(release_info)

        return HttpResponse(status_code=201, body=body_response)
