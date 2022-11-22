from .base import Base
from sqlalchemy import Boolean, Column, DateTime,String,Integer,ForeignKey, func
from sqlalchemy.orm import relationship

class User(Base):

    __tablename__ = "users"

    catalog_id = Column(Integer,ForeignKey("user_catalogs.id"))
    name = Column(String)
    login = Column(String)
    catalog = relationship("UserCatalog",back_populates="users")
    id = Column(Integer,primary_key=True)
    created_utc = Column(DateTime(timezone=True), server_default=func.now())
    is_deleted = Column(Boolean)
    last_updated_by = Column(Integer)
    last_updated_utc = Column(DateTime(timezone=True), server_default=func.now())
    

    # @property
    # def name(self):
    #     return self.__name

    # @property
    # def login(self):
    #     return self.__login

    # @property
    # def user_folder(self):
    #     return self.__user_folder
