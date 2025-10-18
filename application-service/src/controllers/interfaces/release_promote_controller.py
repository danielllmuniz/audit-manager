from typing import Dict
from abc import ABC, abstractmethod

class ReleasePromoteController(ABC):
    @abstractmethod
    def promote(self, release_id: int, user_role: str) -> Dict:
        pass
