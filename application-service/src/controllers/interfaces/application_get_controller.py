from abc import ABC, abstractmethod
from typing import Dict

class ApplicationGetController(ABC):

    @abstractmethod
    def get(self, application_id: int) -> Dict:
        pass
