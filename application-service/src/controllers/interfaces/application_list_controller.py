from typing import Dict
from abc import ABC, abstractmethod

class ApplicationListController(ABC):
    @abstractmethod
    def list(self) -> Dict:
        pass
