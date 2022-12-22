from typing import List, Union
from ..db import create_connection
from fastapi import Depends
from ..file import File, FileType
from sqlalchemy.orm import Session, joinedload
from ...utils.utils import generate_file_key, generate_user_root_key


class FileRepository:
    def __init__(self, db_session: Session = Depends(create_connection)) -> None:
        self.__db_session = db_session

    def get_user_root(self, user_id):
        root_id = self.__db_session.query(File.id) \
            .filter(File.file_type == FileType.DIRECTORY) \
            .filter(File.parent_id == None) \
            .filter(File.name == "root") \
            .filter(File.user_id == user_id)\
            .scalar()
        result = self.get_directory(user_id, root_id)
        return result

    def get_directory(self, user_id, directory_id, with_children=True) -> Union[File, None]:
        result = self.__db_session.query(File) \
            .filter(File.file_type == FileType.DIRECTORY) \
            .filter(File.user_id == user_id) \
            .filter(File.id == directory_id)
        if with_children:
            result = result.options(joinedload(File.children))
        result = result.first()
        return result

    def get_directory_by_key(self, key):
        result = self.__db_session.query(File) \
            .filter(File.file_type == FileType.DIRECTORY) \
            .filter(File.key == key) \
            .first()
        return result

    def get_file(self, user_id, file_id) -> Union[File, None]:
        result = self.__db_session.query(File) \
            .filter(File.file_type == FileType.FILE) \
            .filter(File.user_id == user_id) \
            .filter(File.id == file_id) \
            .first()
        return result

    def get_files(self, user_id, directory_id) -> List[File]:
        result = self.__db_session.query(File) \
            .filter(File.file_type == FileType.FILE) \
            .filter(File.user_id == user_id) \
            .filter(File.parent_id == directory_id) \
            .all()
        return result

    def create_user_root(self, user_id):
        root_key = generate_user_root_key()
        directory = File(file_type=FileType.DIRECTORY,
                         user_id=user_id, key=root_key, name="root")
        self.__db_session.add(directory)
        self.__db_session.commit()
        return directory

    def create_directory(self, user_id, data):
        file_key = generate_file_key(data["name"])
        directory = File(**data, file_type=FileType.DIRECTORY,
                         user_id=user_id, key=file_key)
        self.__db_session.add(directory)
        self.__db_session.commit()
        return directory

    def create_file(self, data):
        file = File(**data, file_type=FileType.FILE)
        self.__db_session.add(file)
        self.__db_session.commit()
        return file

    def delete_directory(self, user_id, directory_id):
        directory = self.get_directory(user_id, directory_id)
        if directory is not None:
            dirs_stack = [directory]
            while dirs_stack:
                current_dir = dirs_stack.pop()
                if current_dir.is_deleted:
                    for child in current_dir.children:
                        if child.file_type == FileType.DIRECTORY:
                            dirs_stack.append(child)
                        elif child.file_type == FileType.FILE:
                            if child.is_deleted:
                                self.__db_session.delete(child)
                self.__db_session.delete(current_dir)
            self.__db_session.commit()
            return True
        return False

    def delete_file(self, user_id, file_id):
        file = self.get_file(user_id, file_id)
        if file is not None:
            if file.is_deleted:
                self.__db_session.delete(file)
                self.__db_session.commit()
                return True
            return False
        return False

    def update_file(self, user_id, file_id, request):
        file = self.get_file(user_id, file_id)
        if file is not None:
            file.name = request.name
            self.__db_session.commit()
            return True
        return False

    def update_directory(self, user_id, directory_id, request):
        directory = self.get_directory(user_id, directory_id)
        if directory is not None:
            directory.name = request.name
            self.__db_session.commit()
            return True
        return False

    def set_status_file(self, user_id, file_id, status) -> bool:
        file = self.get_file(user_id, file_id)
        if file is not None:
            parent = self.get_directory(user_id, file.parent_id)
            if parent is not None:
                if not parent.is_deleted:
                    if file.is_deleted != status:
                        file.is_deleted = status
                else:
                    raise Exception("Invalid operation")
            self.__db_session.commit()
            return True
        return False

    def set_status_directory(self, user_id, directory_id, status) -> bool:
        directory = self.get_directory(user_id, directory_id)
        if directory is not None:
            dirs_stack = [directory]
            while dirs_stack:
                current_dir = dirs_stack.pop()
                if current_dir.is_deleted != status:
                    current_dir.is_deleted = status
                for child in current_dir.children:
                    if child.file_type == FileType.DIRECTORY:
                        dirs_stack.append(child)
                    elif child.file_type == FileType.FILE:
                        if child.is_deleted != status:
                            child.is_deleted = status
            self.__db_session.commit()
            return True
        return False

    # def set_status(self, user_id, file_id) -> bool:
    #     directory = self.get_directory_with_content(user_id, file_id)
    #     if directory is not None:
    #         directory.is_deleted = not directory.is_deleted
    #         for sub_directory in directory.directories:
    #             sub_directory.is_delete
    #         return True
    #     return False
