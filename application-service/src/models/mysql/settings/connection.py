from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base_url import DB_URL
class DBConnectionHandler:
    def __init__(self) -> None:
        self.__connection_string = DB_URL
        self.__engine = None
        self.session = None

    def connect_to_db(self):
        self.__engine = create_engine(self.__connection_string, echo=False, pool_pre_ping=True)

    def get_engine(self):
        return self.__engine

    def __enter__(self):
        session_maker = sessionmaker()
        self.session = session_maker(bind=self.__engine)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

db_connection_handler = DBConnectionHandler()
