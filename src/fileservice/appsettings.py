from functools import lru_cache
import json
from pathlib import Path
from pydantic import BaseSettings


def get_working_dir():
    print("Accessed")
    return Path.cwd().joinpath("fileservice")


class AppSettings(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: int = 8000

    database_url: str

    jwt_secret: str
    jwt_algorithm: str = 'HS256'
    jwt_expires_s: int = 900

    working_dir = get_working_dir()
    users_directories = working_dir.joinpath("UsersDirs")

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return AppSettings()


# class AppSettings:

#     instance = None

#     def __init__(self):
#         self.__working_dir = Path.cwd().joinpath("fileservice")
#         self.__settings_cache = self.__load_settings()
#         self.__override_app_dir(self.get_property("app_dir"))

#     def print_settings(self):
#         for key in self.__settings_cache:
#             print(key, " - ", self.__settings_cache[key])

#     def __load_settings(self, base="app_dir"):
#         settings = json.loads(self.__working_dir.joinpath(
#             "settings.json").read_text())
#         for key in settings.keys():
#             if not key == base:
#                 settings[key] = str(
#                     Path(settings[base]).joinpath(settings[key]))
#         return settings

#     def get_property(self, property_name):
#         if self.__settings_cache is None:
#             self.__settings_cache = self.__load_settings("app_dir")
#         return self.__settings_cache[property_name]

#     def __override_app_dir(self, previous_dir):
#         if str(self.__working_dir) == previous_dir:
#             return
#         else:
#             settings = json.loads(self.__working_dir.joinpath(
#                 "settings.json").read_text())
#             settings["app_dir"] = str(self.__working_dir)
#             Path(self.__working_dir, "settings.json").write_text(
#                 json.dumps(settings))
#             self.__settings_cache = self.__load_settings()

#     @classmethod
#     def get_instance(cls):
#         if cls.instance is None:
#             cls.instance = AppSettings()
#         return cls.instance
