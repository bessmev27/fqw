import json
from pathlib import Path
from deprecated import deprecated


class AppSettings:
    def __init__(self):
        self.__working_dir = Path.cwd()
        self.__settings_cache = self.__load_settings()
        self.__override_app_dir(self.get_property("app_dir"))

    def print_settings(self):
        for key in self.__settings_cache:
            print(key," - ",self.__settings_cache[key])
        
    def __load_settings(self,base="app_dir"):
        settings = json.loads(self.__working_dir.joinpath("settings.json").read_text())
        for key in settings.keys():
            if not key == base:
                settings[key] = str(Path(settings[base]).joinpath(settings[key]))
        return settings

    def get_property(self, property_name):
        if self.__settings_cache is None:
            self.__settings_cache = self.__load_settings("app_dir")
        return self.__settings_cache[property_name]

    def __override_app_dir(self, previous_dir):
        if str(self.__working_dir) == previous_dir:
            return
        else:
            settings = json.loads(self.__working_dir.joinpath("settings.json").read_text())
            settings["app_dir"] = str(self.__working_dir)
            Path(self.__working_dir, "settings.json").write_text(
                json.dumps(settings))
            self.__settings_cache = self.__load_settings()
