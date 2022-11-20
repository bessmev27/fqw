
import os
from pathlib import Path
from models.catalog import UserCatalog

from models.user import User


class UserService:

    def __init__(self, database_connection):
        self.__db = database_connection

    def create_user(self,user_request):
        default_catalog = self.__db.query(UserCatalog).filter(UserCatalog.name=="Default").first()
        new_user = User(user_request["name"],user_request["login"])
        new_user.catalog_id = default_catalog.id
        self.__db.add(new_user)
        self.__db.commit()
        return new_user

    def get_user(self,login):
        result = self.__db.query(User).filter(User.login==login).first()
        if not result is None:
            return result

