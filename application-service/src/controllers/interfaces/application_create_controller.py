from typing import Dict
from abc import ABC, abstractmethod

class ApplicationCreateController(ABC):
    @abstractmethod
    def create(self, application_info: Dict) -> Dict:
        pass
