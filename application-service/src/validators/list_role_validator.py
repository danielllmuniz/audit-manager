from src.views.http_types.http_request import HttpRequest
from src.errors.error_types.http_bad_request import HttpBadRequestError

def list_role_validator(http_request: HttpRequest) -> str:
    headers = http_request.headers or {}
    user_role = headers.get('X-User-Role')

    if not user_role:
        raise HttpBadRequestError("Missing X-User-Role header")

    allowed_roles = ["DEV", "APPROVER", "DEVOPS"]
    if user_role not in allowed_roles:
        raise HttpBadRequestError(
            f"Only users with {', '.join(allowed_roles)} roles can perform this operation"
        )

    return user_role
