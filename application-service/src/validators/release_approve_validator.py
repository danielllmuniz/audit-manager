from typing import Tuple
from src.views.http_types.http_request import HttpRequest
from src.errors.error_types.http_bad_request import HttpBadRequestError

def release_approve_validator(http_request: HttpRequest) -> Tuple[str, str]:
    headers = http_request.headers or {}
    user_role = headers.get('X-User-Role')
    user_email = headers.get('X-User-Email')

    if not user_role:
        raise HttpBadRequestError("Missing X-User-Role header")

    if not user_email:
        raise HttpBadRequestError("Missing X-User-Email header")

    return user_role, user_email
