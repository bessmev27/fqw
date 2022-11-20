import traceback
from services.userservice import UserService
from services.userfolderservice import UserFolderService
from models.appsettings import AppSettings
from models.db import Database
from pathlib import Path
from models.user import User
import os
from tkinter.filedialog import askopenfilename

def main():
    try:
        app_settings = AppSettings()
        db = Database(app_settings)
        if not db.database_exists():
             db.create_database()
        db_connection = db.create_connection()
        user_service = UserService(db_connection)
        user_folder_service = UserFolderService(app_settings,db_connection)
        current_user = user_service.get_user(os.getlogin())
        if current_user is None:
            login = os.getlogin()
            name = input("Enter your name: ")
            request = {"name":name,"login":login}
            current_user = user_service.create_user(request)
            directory_request = {"name":current_user.login,"parent_id": None, "user_id": current_user.id, "create_root": True}
            user_folder_service.create_directory(directory_request)
        directory = user_folder_service.get_directory(current_user.id)
        # request = {
        #     "parent_id": directory.id,
        #     "name": "Test folder",
        #     "user_id": current_user.id
        # }
        filename = askopenfilename()
        request = {
            "dir_id": directory.directories[0].id,
            "name": os.path.basename(filename),
            "content": Path(filename).read_bytes(),
            "size": os.stat(filename).st_size
        }
        user_folder_service.create_file(request)
    except:
        traceback.print_exc()
    finally:
        print("Done")
        #user_folder_service.reindex(current_user.id)

        # fileTree = FileTree(current_user_dir, current_user)


if __name__ == '__main__':
    main()

        # users = app_settings.load_users()
        # logon_user = os.getlogin()
        # if not users:
        #     current_user = User("Evgeny", logon_user, "bessmev")
        #     users.append(current_user)
        #     need_save = True
        # else:
        #     current_user = next(
        #         (u for u in users if u.login == logon_user), None)
        # if current_user is None:
        #     need_add = input(
        #         "Firstly register your user in our system! Do you wanna join?")
        #     if need_add == "y":
        #         current_user = User("Evgeny", logon_user, "bessmev")
        #         users.append(current_user)
        #         need_save = True
        #     return