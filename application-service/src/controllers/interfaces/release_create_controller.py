from typing import Dict
from abc import ABC, abstractmethod

class ReleaseCreateController(ABC):
    @abstractmethod
    def create(self, release_info: Dict) -> Dict:
        pass
