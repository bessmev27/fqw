from fastapi import Depends
from ..database.repository.user import UserRepository
from ..services.disk import DiskService
from ..models.exception import InvalidOperationException,UnexpectedException

class UserService:
    def __init__(self,user_repository: UserRepository = Depends(), disk_service: DiskService = Depends()) -> None:
        self.__user_repository = user_repository
        self.__disk_service = disk_service

    def get_users(self):
        return self.__user_repository.get_users()

    def create_user(self,data):
        existed_user = self.__user_repository.get_user_for_register(
            data.login, data.email)
        if existed_user:
            raise InvalidOperationException(
                "User with given login or email exist")
        result = self.__user_repository.create_user(data.dict())
        root_dir = self.__disk_service.create_user_root(result.id)
        if (result is None) or (root_dir is None):
            raise UnexpectedException("Something went wrong while adding new user")
        return result

    def get_user(self,login,email=None):
        return self.__user_repository.get_user(login,email)    