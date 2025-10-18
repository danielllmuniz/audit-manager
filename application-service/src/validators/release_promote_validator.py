from src.views.http_types.http_request import HttpRequest
from src.errors.error_types.http_bad_request import HttpBadRequestError

def release_promote_validator(http_request: HttpRequest) -> str:
    """
    Valida se o usuário tem a role DEVOPS através do header X-User-Role.
    Retorna a role do usuário.
    """
    headers = http_request.headers or {}
    user_role = headers.get('X-User-Role')

    if not user_role:
        raise HttpBadRequestError("Missing X-User-Role header")

    return user_role
