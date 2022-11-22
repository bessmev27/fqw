from pathlib import Path
from database.directory import Directory
from database.file import File


class UserFolderService:

    def __init__(self,app_settings,database_connection):
        self.__app_settings = app_settings
        self.__root_directory = Path(self.__app_settings.get_property("users_dirs"))
        self.__db = database_connection

    def __make_path(self,dir_id):
        user_dir = self.__db.get(Directory,dir_id)
        part_of_path = [user_dir.name]
        if not user_dir.parent is None:
            parent_id = user_dir.parent_id
            while not parent_id is None:
                temp_dir = self.__db.get(Directory,parent_id)
                part_of_path.append(temp_dir.name)
                parent_id = temp_dir.parent_id
        return self.__root_directory.joinpath(*reversed(part_of_path))

    def create_directory(self,create_directory_request) -> Directory:
        if create_directory_request["parent_id"] is None:
            root_dir = self.__db.query(Directory).filter(Directory.parent_id == None, Directory.user_id == create_directory_request["user_id"]).first()
            if root_dir is None:
                self.__root_directory.joinpath(create_directory_request["name"]).mkdir()
            else: raise Exception("User already has root directory!")
        else:
            self.__make_path(create_directory_request["parent_id"]).joinpath(create_directory_request["name"]).mkdir()
        new_dir = Directory(**create_directory_request)
        self.__db.add(new_dir)
        self.__db.commit()
        return new_dir

    def get_directory(self, user_id,dir_id = None) -> Directory:
        if dir_id is None:
            result = self.__db.query(Directory).filter(Directory.parent_id == None, Directory.user_id == user_id).first()
            if not result is None:
                return result
        result = self.__db.get(Directory,dir_id)
        return result
    
    def get_file(self,file_id) -> File:
        result = self.__db.get(File,file_id)
        return result

    def create_file(self,create_file_request) -> File:
        new_file = File(**create_file_request)
        if not create_file_request["content"] is None:
            self.__make_path(create_file_request["dir_id"]).joinpath(create_file_request["name"]).write_bytes(create_file_request["content"])
        self.__db.add(new_file)
        self.__db.commit()
        return new_file
        

    # def reindex(self,user_id):
    #     root_dir = self.__db.query(Directory).filter(Directory.parent_id == None, Directory.user_id == user_id).first()
    #     if root_dir is None:
    #         raise Exception("User has not have root directory!")
    #     dir_id = root_dir.id
    #     user_dir = self.__make_path(dir_id)
    #     dir_stack = [user_dir]
    #     while dir_stack:
    #         current_dir = dir_stack.pop()
    #         for f in current_dir.iterdir():
    #             if f.is_file():
    #                 file_db = self.__db.query(File).filter(File.name == f.name,File.directory_id == dir_id).first()
    #                 print(f.stat().st_size)
    #                 if file_db is None:
    #                     request = { "name": f.name,
    #                     "dir_id":dir_id,
    #                     "content": None,
    #                     "size": f.stat().st_size
    #                     }
    #                     self.create_file(request)
    #             elif f.is_dir():
    #                 db_dir = self.__db.query(Directory).filter(Directory.name == f.name,Directory.parent_id == dir_id).first()
    #                 if db_dir is None:
    #                     request = {
    #                     "name":f.name,
    #                     "parent_id":dir_id,
    #                     "user_id": user_id,
    #                     "add_to_fs": None
    #                     }
    #                     db_dir = self.create_directory(request)
    #                     dir_id = db_dir.id
    #                     dir_stack.append(f)

