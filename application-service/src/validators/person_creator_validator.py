from pydantic import BaseModel, constr, ValidationError
from src.views.http_types.http_request import HttpRequest
from src.errors.error_types.http_unprocessable_entity import HttpUnprocessableEntityError

def person_creator_validator(http_request: HttpRequest) -> None:
    class BodyData(BaseModel):
        name: constr(min_length=1) # type: ignore
        owner_team: constr(min_length=1)  # type: ignore
        repo_url: constr(min_length=1)  # type: ignore

    try:
        BodyData(**http_request.body)
    except ValidationError as e:
        raise HttpUnprocessableEntityError(e.errors()) from e
