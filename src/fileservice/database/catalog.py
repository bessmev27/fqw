from .base import Base
from sqlalchemy import Boolean, Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship


class UserCatalog(Base):

    __tablename__ = "user_catalogs"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    users = relationship("User", back_populates="catalog")
    created = Column(DateTime(timezone=True), server_default=func.now())
    is_deleted = Column(Boolean)
    last_updated_by = Column(Integer)
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
