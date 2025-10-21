from typing import List, Dict, Any
from src.models.mysql.entities.releases import ReleasesTable, EnvironmentEnum, StatusEnum
from src.models.mysql.interfaces.release_repository import ReleaseRepositoryInterface
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload


class ReleasesRepository(ReleaseRepositoryInterface):
    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection

    def create_release(
        self,
        application_id: int,
        version: str,
        env: EnvironmentEnum,
        evidence_url: str = None,
        status: StatusEnum = StatusEnum.CREATED
    ) -> ReleasesTable:
        with self.__db_connection as database:
            try:
                release_data = ReleasesTable(
                    application_id=application_id,
                    version=version,
                    env=env,
                    status=status,
                    evidence_url=evidence_url
                )
                database.session.add(release_data)
                database.session.commit()
                database.session.refresh(release_data)

                release_with_app = (
                    database.session
                        .query(ReleasesTable)
                        .options(joinedload(ReleasesTable.application))
                        .filter(ReleasesTable.id == release_data.id)
                        .one()
                )

                return release_with_app
            except Exception as e:
                database.session.rollback()
                raise e

    def get_release(self, release_id: int) -> ReleasesTable:
        with self.__db_connection as database:
            try:
                release = (
                    database.session
                        .query(ReleasesTable)
                        .options(joinedload(ReleasesTable.application))
                        .filter(ReleasesTable.id == release_id)
                        .one()
                )
                return release
            except NoResultFound:
                return None

    def list_releases(self) -> List[ReleasesTable]:
        with self.__db_connection as database:
            try:
                releases = (
                    database.session
                        .query(ReleasesTable)
                        .options(joinedload(ReleasesTable.application))
                        .all()
                )
                return releases
            except NoResultFound:
                return []

    def list_releases_by_application(self, application_id: int) -> List[ReleasesTable]:
        with self.__db_connection as database:
            try:
                releases = (
                    database.session
                        .query(ReleasesTable)
                        .options(joinedload(ReleasesTable.application))
                        .filter(ReleasesTable.application_id == application_id)
                        .all()
                )
                return releases
            except NoResultFound:
                return []

    def update_release(self, release_id: int, update_data: Dict[str, Any]) -> ReleasesTable:
        with self.__db_connection as database:
            try:
                release = (
                    database.session
                        .query(ReleasesTable)
                        .filter(ReleasesTable.id == release_id)
                        .one()
                )

                for key, value in update_data.items():
                    if hasattr(release, key):
                        setattr(release, key, value)

                database.session.commit()

                release_with_app = (
                    database.session
                        .query(ReleasesTable)
                        .options(joinedload(ReleasesTable.application))
                        .filter(ReleasesTable.id == release_id)
                        .one()
                )

                return release_with_app
            except NoResultFound:
                return None
            except Exception as e:
                database.session.rollback()
                raise e
