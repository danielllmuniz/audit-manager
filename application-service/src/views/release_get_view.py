from src.controllers.interfaces.release_get_controller import ReleaseGetControllerInterface
from src.views.http_types.http_request import HttpRequest
from src.views.http_types.http_response import HttpResponse


class ReleaseGetView:
    def __init__(self, controller: ReleaseGetControllerInterface) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        release_id = http_request.param["release_id"]
        body_response = self.__controller.get(release_id)
        return HttpResponse(status_code=200, body=body_response)
