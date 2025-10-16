from sqlalchemy import create_engine

class DBConnectionHandler:
    def __init__(self) -> None:
        self.__connection_string = "mysql+pymysql://user:password@localhost:3306/audit_db"
        self.__engine = None

    def connect_to_db(self):
        self.__engine = create_engine(self.__connection_string, echo=False, pool_pre_ping=True)

    def get_engine(self):
        return self.__engine

db_connection_handler = DBConnectionHandler()
