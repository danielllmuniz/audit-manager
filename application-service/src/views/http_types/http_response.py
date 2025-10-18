from typing import Dict

class HttpResponse:
    def __init__(self, status_code: int, body: Dict = None) -> None:
        self.body = body
        self.status_code = status_code
