from typing import List
from src.models.mysql.entities.applications import ApplicationsTable
from src.models.mysql.interfaces.application_repository import ApplicationRepositoryInterface
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload
from sqlalchemy import desc


class ApplicationsRepository(ApplicationRepositoryInterface):
    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection

    def create_application(self, name: str, owner_team: str, repo_url: str = None) -> ApplicationsTable:
        with self.__db_connection as database:
            try:
                application_data = ApplicationsTable(
                    name=name,
                    owner_team=owner_team,
                    repo_url=repo_url
                )
                database.session.add(application_data)
                database.session.commit()
                database.session.refresh(application_data)
                return application_data
            except Exception as e:
                database.session.rollback()
                raise e

    def get_application(self, application_id: int) -> ApplicationsTable:
        with self.__db_connection as database:
            try:
                application = (
                    database.session
                        .query(ApplicationsTable)
                        .options(joinedload(ApplicationsTable.releases))
                        .filter(ApplicationsTable.id == application_id)
                        .one()
                )
                if application.releases:
                    application.releases.sort(key=lambda r: r.created_at, reverse=True)
                return application
            except NoResultFound:
                return None

    def get_application_by_name(self, name: str) -> ApplicationsTable:
        with self.__db_connection as database:
            try:
                application = (
                    database.session
                        .query(ApplicationsTable)
                        .filter(ApplicationsTable.name == name)
                        .one()
                )
                return application
            except NoResultFound:
                return None

    def list_applications(self) -> List[ApplicationsTable]:
        with self.__db_connection as database:
            try:
                applications = (
                    database.session
                        .query(ApplicationsTable)
                        .order_by(desc(ApplicationsTable.created_at))
                        .all()
                )
                return applications
            except NoResultFound:
                return []

    def delete_application(self, name: str) -> None:
        with self.__db_connection as database:
            try:
                (
                    database.session
                        .query(ApplicationsTable)
                        .filter(ApplicationsTable.name == name)
                        .delete()
                )
                database.session.commit()
            except Exception as e:
                database.session.rollback()
                raise e
