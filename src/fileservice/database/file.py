from .base import Base
from sqlalchemy import Boolean, Column, DateTime, String, Integer, ForeignKey, func, Enum
from sqlalchemy.orm import relationship
from ..models.file import FileType

class File(Base):

    __tablename__ = "user_files"

    file_type = Column(Enum(FileType))
    id = Column(Integer, primary_key=True)
    name = Column(String)
    size = Column(Integer)
    content_type = Column(String)
    key = Column(String)

    user_id = Column(Integer, ForeignKey('users.id'))
    parent_id = Column(Integer, ForeignKey("user_files.id"))
    children = relationship("File")

    created = Column(DateTime(timezone=True), server_default=func.now())
    is_deleted = Column(Boolean, default=False)
    modified = Column(DateTime(timezone=True),
                      server_default=func.now(),onupdate=func.now())
