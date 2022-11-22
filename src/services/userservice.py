from typing import List, Optional

from database.catalog import UserCatalog

from database.user import User


class UserService:

    def __init__(self, database_connection):
        self.__db = database_connection

    def get_users(self) -> List[User]:
        return self.__db.query(User).all()

    def create_user(self,user_request) -> User:
        default_catalog = self.__db.query(UserCatalog).filter(UserCatalog.name=="Default").first()
        new_user = User(**user_request)
        new_user.catalog_id = default_catalog.id
        self.__db.add(new_user)
        self.__db.commit()
        return new_user

    def get_user(self,login) -> Optional[User]:
        result = self.__db.query(User).filter(User.login==login).first()
        if not result is None:
            return result

