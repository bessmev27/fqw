from .base import Base
from sqlalchemy import Boolean, Column, DateTime, String, Integer, ForeignKey, Table, func
from sqlalchemy.orm import relationship

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    login = Column(String)
    email = Column(String)
    password = Column("hashed_password", String)

    catalog_id = Column(Integer, ForeignKey("user_catalogs.id"))
    catalog = relationship("UserCatalog", back_populates="users")

    created_utc = Column(DateTime(timezone=True), server_default=func.now())
    is_deleted = Column(Boolean)
    modified = Column(DateTime(timezone=True),
                              server_default=func.now())

class UserCatalog(Base):

    __tablename__ = "user_catalogs"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    users = relationship("User", back_populates="catalog")
    created = Column(DateTime(timezone=True), server_default=func.now())
    is_deleted = Column(Boolean)
    modified = Column(DateTime(timezone=True), server_default=func.now())

# class RefreshToken(Base):
#     __tablename__ = "user_tokens"

#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey="users.id")
#     token = Column(String)
