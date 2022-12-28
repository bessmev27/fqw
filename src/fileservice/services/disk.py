from pathlib import Path
#from typing import List, Optional, Union

from fastapi import Depends
from ..appsettings import AppSettings, get_settings
from ..database.repository.file import FileRepository
from ..models.file import File, FileDownloadResponse, FileType, FileUploadRequest
from ..utils import generate_file_key
from ..models.exception import InvalidOperationException, UnexpectedException


class DiskService:

    def __init__(self,
                 app_settings: AppSettings = Depends(get_settings),
                 file_repository: FileRepository = Depends()):
        self.__root_directory = app_settings.users_directories
        self.__file_repository = file_repository

    def create_user_root(self, user_id):
        existed_root_dir = self.__file_repository.get_user_root(user_id,False)
        if existed_root_dir:
            raise InvalidOperationException(
                "User already has a root directory")
        root_dir_key = generate_file_key("root")
        root_dir = {
            "key": root_dir_key,
            "name": "root"}
        result = self.__file_repository.create_directory(user_id,root_dir)
        self.__root_directory.joinpath(result.key).mkdir()
        return result

    def get_user_root(self, user_id):
        result = self.__file_repository.get_user_root(user_id)
        if result is None:
            # if this error occurs it means what created user was incorrect processed
            raise ValueError("User does not have root directory")
        return result


    def get_directory(self, user_id, directory_id):
        directory = self.__file_repository \
            .get_directory(user_id, directory_id)
        if directory is None:
            raise ValueError("Directory with given id does not exist")
        return directory

    def create_directory(self, user_id, create_request):
        request_dict = create_request.dict()
        directory_key = generate_file_key(create_request.name)
        request_dict.update({"key": directory_key})
        parent = self.__file_repository.get_directory(
            user_id, create_request.parent_id,False)
        if parent is None:
            raise ValueError("Parent directory with given id does not exist")
        directory_path = self.__make_hierarchy(user_id, parent.id)
        new_directory = self.__file_repository.create_directory(user_id,request_dict)
        if new_directory is None:
            raise UnexpectedException("Something went wrong while adding new directory")
        directory_path.joinpath(new_directory.key).mkdir()
        return new_directory

    def move_file(self, request):
        pass

    def download_file(self, user_id, file_id):
        result = self.__file_repository.get_file(user_id, file_id)
        if result is None:
            raise ValueError("File with given id does not exist")
        file_path = self.__make_hierarchy(
            user_id, result.parent_id).joinpath(result.key)
        file_name = result.name
        response = FileDownloadResponse(name=file_name, path=str(file_path))
        return response

    def upload_file(self, user_id, parent_id, files):
        result = []
        parent = self.__file_repository.get_directory(
            user_id, parent_id)
        if parent is None:
            raise ValueError("Parent directory with given id does not exist")
        file_path = self.__make_hierarchy(
            user_id, parent.id)
        for file in files:
            content = file.file.read()
            file_key = generate_file_key(file.filename)
            file_to_add = FileUploadRequest(name=file.filename,
                                            size=len(content),
                                            content_type=file.content_type,
                                            parent_id=parent_id,
                                            key=file_key)
            processed_file = self.__file_repository.create_file(user_id,
                file_to_add.dict())
            if processed_file is None:
                raise UnexpectedException("Something went wrong while adding new directory")
            file_path.joinpath(file_key).write_bytes(content)
            result.append(processed_file)
        return result

    def set_status_directory(self, user_id, directory_id, deleted_status):
        root = self.__file_repository.get_user_root(user_id,False)
        if root.id == directory_id:
            raise InvalidOperationException("Directory with given id cannot be processed")
        directory = self.__file_repository.get_directory(
            user_id, directory_id, False)
        if directory is None:
            raise ValueError("Directory with given id does not exist")
        if directory.is_deleted != deleted_status:
            return self.__file_repository.set_status_directory(user_id, directory_id, deleted_status)
        

    def set_status_file(self, user_id, file_id, deleted_status):
        file = self.__file_repository.get_file(
            user_id, file_id)
        if file is None:
            raise ValueError("File with given id does not exist")
        parent = self.get_directory(user_id, file.parent_id)
        if parent is None:
            raise ValueError("File must contain parent")
        if parent.is_deleted:
            raise InvalidOperationException("Parent directory already deleted")
        if file.is_deleted != deleted_status:
            return self.__file_repository.set_status_file(user_id,file_id,deleted_status)

    def rename_file(self, user_id, file_id, request):
        file = self.__file_repository.get_file(user_id,file_id)
        if file is None:
            raise ValueError("File with given id does not exist")
        result = self.__file_repository.update_file(user_id, file_id, request.dict())
        return result

    def rename_directory(self, user_id, file_id, request):
        root = self.__file_repository.get_user_root(user_id,False)
        if root.id == file_id:
            raise InvalidOperationException("Directory with given id cannot be processed")
        directory = self.__file_repository.get_directory(user_id,file_id,False)
        if directory is None:
            raise ValueError("Directory with given id does not exist")
        result = self.__file_repository.update_directory(user_id, file_id, request.dict())
        return result

    def delete_directory(self, user_id, directory_id):
        directory = self.__file_repository.get_directory(
            user_id, directory_id, False)
        if directory is None:
            raise ValueError("Directory with given id does not exist")
        if not directory.is_deleted:
            raise InvalidOperationException("Confirm deleting by set status first")
        dir_path = self.__make_hierarchy(user_id, directory.id)
        result = self.__file_repository.delete_directory(user_id, directory.id)
        self.__delete_directory_helper(dir_path)
        return result

    def delete_file(self, user_id, file_id):
        file = self.__file_repository.get_file(user_id, file_id)
        if file is None:
            raise ValueError("File with given id does not exist")
        if not file.is_deleted:
            raise InvalidOperationException("Confirm deleting by set status first")
        file_path = self.__make_hierarchy(
            user_id, file.parent_id).joinpath(file.key)
        result = self.__file_repository.delete_file(user_id, file.id)
        file_path.unlink()
        return result

    def __make_path(self, items):
        result = self.__root_directory
        keys = [item.key for item in items]
        return result.joinpath(*reversed(keys))

    def __make_hierarchy(self, user_id, directory_id):
        result = []
        directory = self.__file_repository.get_directory(
            user_id, directory_id)
        result.append(directory)
        if directory.parent_id is None:
            return self.__make_path(result)
        while True:
            parent = self.__file_repository.get_directory(
                user_id, directory.parent_id)
            result.append(parent)
            if parent.parent_id is None:
                break
            directory = parent
        return self.__make_path(result)

    def refresh(self):
        pass
        print("Starting refresh userdirs")
        result = 0
        ignore = "bessmev"
        for user_scope in self.__root_directory.iterdir():
            if not user_scope.name == ignore:
                db_item = self.__file_repository.get_user_root_by_key(
                    user_scope.name)
                if db_item is None:
                    print(
                        f"{user_scope.name} dont exists in database. Removing dir...")
                    result = result + 1
                    self.__delete_directory_helper(user_scope)
        print("Refresh success! Count deleted items: ", result)

    def __delete_directory_helper(self, pth: Path):
        for sub in pth.iterdir():
            if sub.is_dir():
                self.__delete_directory_helper(sub)
            else:
                sub.unlink()
        pth.rmdir()  # if you just want to delete the dir content but not the dir itself, remove this line
