from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
import os
from models.catalog import UserCatalog

from models.user import User
from models.catalog import UserCatalog


class Database:


    def __init__(self,app_settings) -> None:
        self.SQLALCHEMY_DATABASE_URL = f"sqlite:///{app_settings.get_property('app_db')}"
        self.SQLALCHEMY_DATABASE_PATH = app_settings.get_property("app_db")
        self.engine = create_engine(
        self.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
        self.session_local = sessionmaker(autoflush=False, bind=self.engine)


    def create_database(self):
        print("Creating database!")
        Base.metadata.create_all(bind=self.engine)
        temp_con = self.create_connection()
        catalog = UserCatalog("Default")
        temp_con.add(catalog)
        temp_con.commit()
    
    
    def create_connection(self):
        return self.session_local()


    def database_exists(self):
        return os.path.exists(self.SQLALCHEMY_DATABASE_PATH)
