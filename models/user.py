from models.base import Base
from sqlalchemy import Column,String,Integer,ForeignKey
from sqlalchemy.orm import relationship

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    catalog_id = Column(Integer,ForeignKey("user_catalogs.id"))
    name = Column(String)
    login = Column(String)
    catalog = relationship("UserCatalog",back_populates="users")
    
    def __init__(self, name, login):
        self.name = name
        self.login = login

    # @property
    # def name(self):
    #     return self.__name

    # @property
    # def login(self):
    #     return self.__login

    # @property
    # def user_folder(self):
    #     return self.__user_folder
