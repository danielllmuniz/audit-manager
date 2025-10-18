from typing import Dict
from abc import ABC, abstractmethod

class ReleaseApproveController(ABC):
    @abstractmethod
    def approve(self, release_id: int, user_role: str) -> Dict:
        pass
