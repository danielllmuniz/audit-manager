from typing import Dict, Optional
from abc import ABC, abstractmethod

class ReleaseListController(ABC):
    @abstractmethod
    def list(self, application_id: Optional[int] = None) -> Dict:
        pass
