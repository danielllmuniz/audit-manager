from abc import ABC, abstractmethod
from typing import List
from src.models.mysql.entities.approvals import ApprovalsTable, OutcomeEnum

class ApprovalRepositoryInterface(ABC):
    @abstractmethod
    def create_approval(
        self,
        release_id: int,
        approver_email: str,
        outcome: OutcomeEnum,
        notes: str = None
    ) -> ApprovalsTable:
        pass

    @abstractmethod
    def get_approval(self, approval_id: int) -> ApprovalsTable:
        pass

    @abstractmethod
    def list_approvals_by_release(self, release_id: int) -> List[ApprovalsTable]:
        pass
