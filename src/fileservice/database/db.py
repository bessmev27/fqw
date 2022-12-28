
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists

from sqlalchemy.orm import sessionmaker

from .base import Base
from ..appsettings import AppSettings, get_settings


app_settings = get_settings()

SQLALCHEMY_DATABASE_URL = app_settings.database_url
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
session_builder = sessionmaker(autoflush=False, bind=engine)



def exists():
    return database_exists(engine.url)


def create_if_not_exists(initializer=None):
    if not exists():
        Base.metadata.create_all(bind=engine)


def create_connection():
    try:
        session = session_builder()
        yield session
    finally:
        session.close()
