from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .base_url import DB_URL

class DBConnectionHandler:
    def __init__(self) -> None:
        self.__connection_string = DB_URL
        self.__engine = None
        self.__session_factory = None

    def connect_to_db(self):
        self.__engine = create_engine(
            self.__connection_string,
            echo=False,
            pool_pre_ping=True,
            pool_recycle=3600,
            pool_size=10,
            max_overflow=20
        )
        session_maker = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        self.__session_factory = scoped_session(session_maker)

    def get_engine(self):
        return self.__engine

    @property
    def session(self):
        return self.__session_factory()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:
                self.session.rollback()
            self.session.close()
        finally:
            self.__session_factory.remove()

db_connection_handler = DBConnectionHandler()
