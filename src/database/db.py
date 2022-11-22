import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base

from .catalog import UserCatalog



class Database:

    def __init__(self,app_settings) -> None:
        self.SQLALCHEMY_DATABASE_URL = f"sqlite:///{app_settings.get_property('app_db')}"
        self.SQLALCHEMY_DATABASE_PATH = app_settings.get_property("app_db")
        self.engine = create_engine(
        self.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
        self.Session = sessionmaker(autoflush=False, bind=self.engine)


    def create_database(self):
        print("Creating database!")
        Base.metadata.create_all(bind=self.engine)
        catalog = UserCatalog(name="Default")
        temp_con = next(self.create_connection())
        temp_con.add(catalog)
        temp_con.commit()
    
    
    def create_connection(self):
        try:
            session = self.Session()
            yield session
        finally:
            session.close()


    def database_exists(self):
        return os.path.exists(self.SQLALCHEMY_DATABASE_PATH)
