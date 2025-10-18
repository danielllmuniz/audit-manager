from typing import Dict
from abc import ABC, abstractmethod

class ReleaseListController(ABC):
    @abstractmethod
    def list(self) -> Dict:
        pass
