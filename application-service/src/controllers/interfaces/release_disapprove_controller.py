from typing import Dict
from abc import ABC, abstractmethod

class ReleaseDisapproveController(ABC):
    @abstractmethod
    def disapprove(self, release_id: int, user_role: str, user_email: str) -> Dict:
        pass
