from typing import List, Optional

from fastapi import Depends

from ..user import User
from sqlalchemy import select,or_,func

from sqlalchemy.orm import Session

from ..db import create_connection



class UserRepository:

    def __init__(self, database_connection: Session = Depends(create_connection)):
        self.__db_session = database_connection

    def get_users(self) -> List[User]:
        stmt = select(User)
        result = self.__db_session.scalars(stmt)
        return result

    def create_user(self, user_request) -> User:
        new_user = User(**user_request)
        self.__db_session.add(new_user)
        self.__db_session.commit()
        return new_user

    def get_user(self, login, email=None) -> Optional[User]:
        filters = [User.login == login]
        stmt = select(
            User)
        if email:
            filters.append(User.email == email)
        stmt = stmt.where(*filters)
        result = self.__db_session.scalar(stmt)
        return result
    
    def get_user_for_register(self,login,email):
        filters = [User.login == login, User.email == email]
        stmt = select(func.count(User.id)).where(or_(*filters))
        result = self.__db_session.scalar(stmt)
        return result
