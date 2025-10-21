from typing import Dict
from abc import ABC, abstractmethod


class ReleaseGetControllerInterface(ABC):
    @abstractmethod
    def get(self, release_id: int) -> Dict:
        pass
