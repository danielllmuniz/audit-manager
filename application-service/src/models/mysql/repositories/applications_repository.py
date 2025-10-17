from typing import List
from src.models.mysql.entities.applications import ApplicationsTable
from sqlalchemy.orm.exc import NoResultFound

class ApplicationsRepository:
    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection

    def list_applications(self) -> List[ApplicationsTable]:
        with self.__db_connection as database:
            try:
                applications = database.session.query(ApplicationsTable).all()
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
