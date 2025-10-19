from typing import List
from src.models.mysql.entities.approvals import ApprovalsTable, OutcomeEnum
from src.models.mysql.interfaces.approval_repository import ApprovalRepositoryInterface
from sqlalchemy.orm.exc import NoResultFound


class ApprovalsRepository(ApprovalRepositoryInterface):
    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection

    def create_approval(
        self,
        release_id: int,
        approver_email: str,
        outcome: OutcomeEnum,
        notes: str = None
    ) -> ApprovalsTable:
        with self.__db_connection as database:
            try:
                approval_data = ApprovalsTable(
                    release_id=release_id,
                    approver_email=approver_email,
                    outcome=outcome,
                    notes=notes
                )
                database.session.add(approval_data)
                database.session.commit()
                database.session.refresh(approval_data)
                return approval_data
            except Exception as e:
                database.session.rollback()
                raise e

    def get_approval(self, approval_id: int) -> ApprovalsTable:
        with self.__db_connection as database:
            try:
                approval = (
                    database.session
                        .query(ApprovalsTable)
                        .filter(ApprovalsTable.id == approval_id)
                        .one()
                )
                return approval
            except NoResultFound:
                return None

    def list_approvals_by_release(self, release_id: int) -> List[ApprovalsTable]:
        with self.__db_connection as database:
            try:
                approvals = (
                    database.session
                        .query(ApprovalsTable)
                        .filter(ApprovalsTable.release_id == release_id)
                        .all()
                )
                return approvals
            except NoResultFound:
                return []
