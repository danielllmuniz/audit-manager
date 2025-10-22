import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.models.mysql.settings.base import Base


@pytest.fixture(scope="function")
def in_memory_db():
    engine = create_engine("sqlite:///:memory:", echo=False)

    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(bind=engine)

    yield SessionLocal

    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(in_memory_db):
    session = in_memory_db()

    try:
        yield session
    finally:
        session.rollback()
        session.close()


class DBConnectionContext:
    def __init__(self, session: Session):
        self.session = session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        _ = exc_val, exc_tb
        if exc_type is not None:
            self.session.rollback()
        return False


@pytest.fixture(scope="function")
def db_connection(db_session):
    return DBConnectionContext(db_session)
