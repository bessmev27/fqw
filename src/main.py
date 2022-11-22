import traceback
from appsettings import AppSettings
from services.userservice import UserService
from services.userfolderservice import UserFolderService
from database.db import Database
from pathlib import Path
import os
from models.user import User

def main():
    try:
        app_settings = AppSettings()
        db = Database(app_settings)
        if not db.database_exists():
             db.create_database()
        db_connection = next(db.create_connection())
        user_service = UserService(db_connection)
        user_folder_service = UserFolderService(app_settings,db_connection)
        current_user = user_service.get_user(os.getlogin())
        if current_user is None:
            login = os.getlogin()
            name = input("Enter your name: ")
            request = {"name":name,"login":login}
            current_user = user_service.create_user(request)
            #directory_request = {"name":current_user.login,"parent_id": None, "user_id": current_user.id, "create_root": True}
            #user_folder_service.create_directory(directory_request)
        #directory = user_folder_service.get_directory(current_user.id)
        print(User.from_orm(current_user))
        # request = {
        #     "parent_id": directory.id,
        #     "name": "Test folder",
        #     "user_id": current_user.id
        # }
        #user_folder_service.create_file(request)
    except:
        traceback.print_exc()
    finally:
        print("Done")
        #user_folder_service.reindex(current_user.id)

        # fileTree = FileTree(current_user_dir, current_user)


if __name__ == '__main__':
    main()
