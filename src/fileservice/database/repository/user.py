from typing import List, Optional

from fastapi import Depends

from ..catalog import UserCatalog

from ..user import User

from sqlalchemy.orm import Session

from ..db import create_connection

from ...models.user import UserCreate


class UserRepository:

    def __init__(self, database_connection: Session = Depends(create_connection)):
        self.__db_session = database_connection

    def get_users(self) -> List[User]:
        return self.__db_session.query(User).all()

    def create_user(self, user_request) -> User:
        new_user = User(**user_request)
        self.__db_session.add(new_user)
        self.__db_session.commit()
        return new_user

    def get_user(self, login) -> Optional[User]:
        result = self.__db_session.query(
            User).filter(User.login == login).first()
        if not result is None:
            return result
