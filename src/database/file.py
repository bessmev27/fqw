from .base import Base
from sqlalchemy import Boolean, Column, DateTime,String,Integer,ForeignKey, func
from sqlalchemy.orm import relationship

class File(Base):

    __tablename__ = "user_files"
    
    id = Column(Integer,primary_key=True)
    name = Column(String)
    size = Column(Integer)
    directory_id = Column(Integer,ForeignKey("user_directories.id"))
    directory = relationship("Directory",back_populates="files")
    created_utc = Column(DateTime(timezone=True), server_default=func.now())
    is_deleted = Column(Boolean)
    last_updated_by = Column(Integer)
    last_updated_utc = Column(DateTime(timezone=True), server_default=func.now())
   
    def __repr__(self) -> str:
        return f"name = {self.name} ; size = {self.size}"