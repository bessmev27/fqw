from pathlib import Path
#from typing import List, Optional, Union

from fastapi import Depends
from ..appsettings import AppSettings, get_settings
from ..database.repository.file import FileRepository
from ..models.file import File, FileDownloadResponse
from ..utils import generate_file_key


class DiskService:

    def __init__(self,
                 app_settings: AppSettings = Depends(get_settings),
                 file_repository: FileRepository = Depends()):
        self.__root_directory = app_settings.users_directories
        self.__file_repository = file_repository

    def create_user_root(self, user_id):
        root_dir = self.__file_repository.create_user_root(user_id)
        self.__root_directory.joinpath(root_dir.key).mkdir()

    def get_user_root(self, user_id):
        result = self.__file_repository.get_user_root(user_id)
        if result is not None:
            return result
        return None

    def get_directory(self, user_id, directory_id):
        directory = self.__file_repository \
            .get_directory(user_id, directory_id)
        if directory is not None:
            return directory
        return None

    def create_directory(self, user_id, create_request):
        print("DirectoryId", create_request.parent_id)
        parent = self.__file_repository.get_directory(
            user_id, create_request.parent_id)
        if parent is None:
            raise Exception("Invalid parent id")
        directory_path = self.__make_hierarchy(user_id, parent.id)
        new_directory = self.__file_repository.create_directory(
            user_id, create_request.dict())
        directory_path.joinpath(new_directory.key).mkdir()
        return new_directory

    def move_file(self, request):
        pass

    def download_file(self, user_id, file_id):
        result = self.__file_repository.get_file(user_id, file_id)
        file_path = self.__make_hierarchy(
            user_id, result.parent_id).joinpath(result.key)
        file_name = result.name
        response = FileDownloadResponse(name=file_name, path=str(file_path))
        return response

    # def get_file(self, user_id, file_key):
    #     file = self.__db_session.query(File).where(File.key == file_key,File.user_id == user_id).first()
    #     parent_key = None
    #     if file.is_dir:
    #         result = self.__db_session.query(File).where(File.parent_id == file.id).all()
    #         parent_key = file.key
    #     else:
    #         result = file
    #         if file.parent_id:
    #             parent_key = self.__db_session.query(File.key).filter(File.id == file.parent_id).scalar()
    #     return FileGetResponse(parent_key=parent_key,data=result)

    def set_status_directory(self, user_id, directory_id, deleted_status):
        return self.__file_repository.set_status_directory(user_id, directory_id, deleted_status)

    def set_status_file(self, user_id, file_id, deleted_status):
        return self.__file_repository.set_status_file(user_id, file_id, deleted_status)

    def rename_file(self, user_id, file_id, request):
        return self.__file_repository.update_file(user_id, file_id, request)

    def rename_directory(self, user_id, file_id, request):
        return self.__file_repository.update_directory(user_id, file_id, request)

    def delete_directory(self, user_id, directory_id):
        directory = self.__file_repository.get_directory(
            user_id, directory_id, False)
        dir_path = self.__make_hierarchy(user_id, directory.id)
        result = self.__file_repository.delete_directory(user_id, directory.id)
        if result:
            self.__delete_directory_helper(dir_path)
            return True
        return False

    def delete_file(self, user_id, file_id):
        file = self.__file_repository.get_file(user_id, file_id)
        file_path = self.__make_hierarchy(
            user_id, file.parent_id).joinpath(file.key)
        result = self.__file_repository.delete_file(user_id, file.id)
        if result:
            file_path.unlink()
            return True
        return False

    def upload_file(self, user_id, upload_request, files):
        result = []
        parent = self.__file_repository.get_directory(
            user_id, upload_request.parent_id)
        if parent is None:
            raise Exception("Invalid parent id")
        file_path = self.__make_hierarchy(
            user_id, parent.id)
        for file in files:
            content = file.file.read()
            file_key = generate_file_key(file.filename)
            file_path.joinpath(file_key).write_bytes(content)
            to_add = {}
            to_add['name'] = file.filename
            to_add['size'] = len(content)
            to_add['content_type'] = file.content_type
            to_add['parent_id'] = parent.id
            to_add['user_id'] = user_id
            to_add['key'] = file_key
            new_file = self.__file_repository.create_file(to_add)
            result.append(new_file)
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
        #print([res.key for res in result])
        return self.__make_path(result)

    def refresh(self):
        print("Starting refresh userdirs")
        result = 0
        ignore = "bessmev"
        for user_scope in self.__root_directory.iterdir():
            if not user_scope.name == ignore:
                db_item = self.__file_repository.get_directory_by_key(
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
