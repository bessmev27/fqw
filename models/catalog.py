from models.base import Base
from sqlalchemy import Column,String,Integer,ForeignKey
from sqlalchemy.orm import relationship

class UserCatalog(Base):

    __tablename__ = "user_catalogs"
    id = Column(Integer,primary_key=True)
    name = Column(String)
    users = relationship("User",back_populates="catalog")

    def __init__(self,name):
        self.name = name