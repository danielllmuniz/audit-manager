from pydantic import BaseModel, constr, ValidationError
from src.views.http_types.http_request import HttpRequest
from src.errors.error_types.http_unprocessable_entity import HttpUnprocessableEntityError

def release_creator_validator(http_request: HttpRequest) -> None:
    class BodyData(BaseModel):
        application_id: int
        version: constr(min_length=1) # type: ignore
        env: str = None  # type: ignore
        evidence_url: str = None  # type: ignore

    try:
        BodyData(**http_request.body)
    except ValidationError as e:
        raise HttpUnprocessableEntityError(e.errors()) from e
