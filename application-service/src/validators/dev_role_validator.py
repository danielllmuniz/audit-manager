from src.views.http_types.http_request import HttpRequest
from src.errors.error_types.http_bad_request import HttpBadRequestError

def dev_role_validator(http_request: HttpRequest) -> str:
    headers = http_request.headers or {}
    user_role = headers.get('X-User-Role')

    if not user_role:
        raise HttpBadRequestError("Missing X-User-Role header")

    if user_role != "DEV":
        raise HttpBadRequestError("Only users with DEV role can perform this operation")

    return user_role
