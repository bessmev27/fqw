from models.base import Base
from sqlalchemy import Column,String,Integer,ForeignKey,DateTime,sql
from sqlalchemy.orm import relationship

class File(Base):

    __tablename__ = "user_files"
    id = Column(Integer,primary_key=True)
    name = Column(String)
    size = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now())
    directory_id = Column(Integer,ForeignKey("user_directories.id"))
    directory = relationship("Directory",back_populates="files")

    def __init__(self,directory_id,name,size):
        self.directory_id = directory_id
        self.name = name
        self.size = size
    
    def __repr__(self) -> str:
        return f"name = {self.name} ; size = {self.size}"