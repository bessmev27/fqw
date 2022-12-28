from typing import Dict, List, Union

from sqlalchemy import select,update,func,insert
from ..db import create_connection
from fastapi import Depends
from ..file import File, FileType
from sqlalchemy.orm import Session, joinedload
from ...models.exception import InvalidOperationException

class FileRepository:
    def __init__(self, db_session: Session = Depends(create_connection)) -> None:
        self.__db_session = db_session

    def get_user_root(self, user_id, with_children=True):
        root_id = self.__db_session.query(File.id) \
            .filter(File.file_type == FileType.DIRECTORY) \
            .filter(File.parent_id == None) \
            .filter(File.name == "root") \
            .filter(File.user_id == user_id) \
            .scalar()
        result = self.get_directory(user_id, root_id, with_children)
        return result
    
    def get_user_root_by_key(self,key):
        stmt = select(File).where(File.name == "root", File.key == key)
        result = self.__db_session.scalar(stmt)
        return result

    def get_directory(self,user_id,directory_id,with_children=True):
        return self.__get_file_base(user_id,directory_id,FileType.DIRECTORY,with_children)
    
    def get_file(self,user_id,file_id):
        return self.__get_file_base(user_id,file_id,FileType.FILE)

    def __get_file_base(self, user_id, file_id,file_type,with_children=True,additional_filters = []) -> Union[File, None]:
        base_filters = [File.file_type == file_type,
        File.user_id == user_id,
        File.id == file_id]
        base_filters.extend(additional_filters)
        stmt = select(File) \
            .where(*base_filters)
        if file_type == FileType.DIRECTORY and with_children:
            stmt = stmt.options(joinedload(File.children))
        result = self.__db_session.scalar(stmt)
        return result


    def get_files(self, user_id, directory_id) -> List[File]:
        stmt = select(File) \
            .where(File.file_type == FileType.FILE,
            File.parent_id == directory_id,
            File.user_id == user_id)
        result = self.__db_session.scalars(stmt)
        return result

    def __create_file_base(self,user_id,file_type,data):
        file = File(**data,file_type=file_type,user_id=user_id)
        self.__db_session.add(file)
        self.__db_session.commit()
        return file
             
    def create_directory(self, user_id, data) -> File:
        return self.__create_file_base(user_id,FileType.DIRECTORY,data)


    def create_file(self, user_id, data) -> File:
        return self.__create_file_base(user_id,FileType.FILE,data)
    

    def delete_directory(self, user_id, directory_id):
        directory = self.get_directory(user_id, directory_id)
        if directory is not None:
            dirs_stack = [directory]
            while dirs_stack:
                current_dir = dirs_stack.pop()
                if current_dir.is_deleted:
                    self.__db_session.delete(current_dir)
                    for child in current_dir.children:
                        if child.file_type == FileType.DIRECTORY:
                            dirs_stack.append(child)
                        elif child.file_type == FileType.FILE:
                            if child.is_deleted:
                                self.__db_session.delete(child)
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


    def __update_file_base(self,user_id,file_id,file_type,request: Dict):
        stmt = update(File) \
            .where(File.user_id == user_id,
            File.file_type == file_type,
            File.id == file_id) \
            .values(**request)
        result = self.__db_session.execute(stmt)
        self.__db_session.commit()
        return result.rowcount
    

    def update_file(self, user_id, file_id, request):
        return self.__update_file_base(user_id,file_id,FileType.FILE,request)
    

    def update_directory(self, user_id, directory_id, request):
        return self.__update_file_base(user_id,directory_id,FileType.DIRECTORY,request)
    

    def set_status_file(self, user_id, file_id, status) -> bool:
        return self.__update_file_base(user_id,file_id,FileType.FILE,{"is_deleted": status})


#Here is should be a cte statements but i so dumb to write it
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