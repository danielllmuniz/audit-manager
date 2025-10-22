from unittest import mock
from datetime import datetime, timezone
import pytest
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from sqlalchemy.orm.exc import NoResultFound
from src.models.mysql.entities.approvals import ApprovalsTable, OutcomeEnum
from .approvals_repository import ApprovalsRepository


class MockConnection:
    def __init__(self, approval_data=None) -> None:
        if approval_data is None:
            approval_data = [
                ApprovalsTable(
                    id=1,
                    release_id=1,
                    approver_email="approver1@example.com",
                    outcome=OutcomeEnum.APPROVED,
                    notes="Looks good",
                    timestamp=datetime.now(timezone.utc)
                ),
                ApprovalsTable(
                    id=2,
                    release_id=1,
                    approver_email="approver2@example.com",
                    outcome=OutcomeEnum.APPROVED,
                    notes=None,
                    timestamp=datetime.now(timezone.utc)
                ),
                ApprovalsTable(
                    id=3,
                    release_id=2,
                    approver_email="approver3@example.com",
                    outcome=OutcomeEnum.REJECTED,
                    notes="Security concerns",
                    timestamp=datetime.now(timezone.utc)
                ),
            ]

        self.session = UnifiedAlchemyMagicMock(
            data=[
                (
                    [mock.call.query(ApprovalsTable)],
                    approval_data,
                )
            ]
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class MockConnectionNoResult:
    def __init__(self) -> None:
        self.session = UnifiedAlchemyMagicMock()
        self.session.query.side_effect = self.__raise_no_result_found

    def __raise_no_result_found(self, *args, **kwargs):
        raise NoResultFound("No result found")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class MockConnectionError:
    def __init__(self) -> None:
        self.session = UnifiedAlchemyMagicMock()
        self.session.add.side_effect = Exception("Database error")
        self.session.commit.side_effect = Exception("Database error")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def test_create_approval():
    mock_connection = MockConnection()
    repo = ApprovalsRepository(mock_connection)

    approval = repo.create_approval(
        release_id=1,
        approver_email="test@example.com",
        outcome=OutcomeEnum.APPROVED,
        notes="Test approval"
    )

    mock_connection.session.add.assert_called_once()
    mock_connection.session.commit.assert_called_once()
    mock_connection.session.refresh.assert_called_once()
    mock_connection.session.rollback.assert_not_called()

    assert approval is not None


def test_create_approval_without_notes():
    mock_connection = MockConnection()
    repo = ApprovalsRepository(mock_connection)

    approval = repo.create_approval(
        release_id=1,
        approver_email="test@example.com",
        outcome=OutcomeEnum.REJECTED,
        notes=None
    )

    mock_connection.session.add.assert_called_once()
    mock_connection.session.commit.assert_called_once()
    mock_connection.session.refresh.assert_called_once()
    mock_connection.session.rollback.assert_not_called()

    assert approval is not None


def test_create_approval_error():
    mock_connection = MockConnectionError()
    repo = ApprovalsRepository(mock_connection)

    with pytest.raises(Exception):
        repo.create_approval(
            release_id=1,
            approver_email="test@example.com",
            outcome=OutcomeEnum.APPROVED,
            notes="Test"
        )

    mock_connection.session.rollback.assert_called_once()


def test_get_approval():
    single_approval = [
        ApprovalsTable(
            id=1,
            release_id=1,
            approver_email="approver1@example.com",
            outcome=OutcomeEnum.APPROVED,
            notes="Looks good",
            timestamp=datetime.now(timezone.utc)
        )
    ]

    mock_connection = MockConnection(approval_data=single_approval)
    repo = ApprovalsRepository(mock_connection)

    approval = repo.get_approval(1)

    mock_connection.session.query.assert_called_with(ApprovalsTable)
    mock_connection.session.query().filter.assert_called_once()
    mock_connection.session.query().filter().one.assert_called_once()

    assert approval is not None
    assert approval.id == 1
    assert approval.approver_email == "approver1@example.com"


def test_get_approval_not_found():
    mock_connection = MockConnectionNoResult()
    repo = ApprovalsRepository(mock_connection)

    approval = repo.get_approval(999)

    assert approval is None
    mock_connection.session.query.assert_called_once_with(ApprovalsTable)


def test_list_approvals_by_release():
    release1_approvals = [
        ApprovalsTable(
            id=1,
            release_id=1,
            approver_email="approver1@example.com",
            outcome=OutcomeEnum.APPROVED,
            notes="Looks good",
            timestamp=datetime.now(timezone.utc)
        ),
        ApprovalsTable(
            id=2,
            release_id=1,
            approver_email="approver2@example.com",
            outcome=OutcomeEnum.APPROVED,
            notes=None,
            timestamp=datetime.now(timezone.utc)
        ),
    ]

    mock_connection = MockConnection(approval_data=release1_approvals)
    repo = ApprovalsRepository(mock_connection)

    approvals = repo.list_approvals_by_release(1)

    mock_connection.session.query.assert_called_with(ApprovalsTable)
    mock_connection.session.query().filter.assert_called_once()
    mock_connection.session.query().filter().all.assert_called_once()

    assert len(approvals) == 2
    assert all(a.release_id == 1 for a in approvals)


def test_list_approvals_by_release_no_results():
    mock_connection = MockConnectionNoResult()
    repo = ApprovalsRepository(mock_connection)

    approvals = repo.list_approvals_by_release(999)

    assert approvals == []
    mock_connection.session.query.assert_called_once_with(ApprovalsTable)


def test_list_approvals_by_release_with_rejected():
    # Test with a mix of approved and rejected
    mixed_approvals = [
        ApprovalsTable(
            id=1,
            release_id=2,
            approver_email="approver1@example.com",
            outcome=OutcomeEnum.APPROVED,
            notes="Good to go",
            timestamp=datetime.now(timezone.utc)
        ),
        ApprovalsTable(
            id=2,
            release_id=2,
            approver_email="approver2@example.com",
            outcome=OutcomeEnum.REJECTED,
            notes="Security issues found",
            timestamp=datetime.now(timezone.utc)
        ),
    ]

    mock_connection = MockConnection(approval_data=mixed_approvals)
    repo = ApprovalsRepository(mock_connection)

    approvals = repo.list_approvals_by_release(2)

    assert len(approvals) == 2
    assert approvals[0].outcome == OutcomeEnum.APPROVED
    assert approvals[1].outcome == OutcomeEnum.REJECTED
