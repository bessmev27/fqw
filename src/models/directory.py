#from datetime import datetime
from json import JSONEncoder

from .base import BasePydanticModel

from .directory import Directory

from .file import File


class Directory(BasePydanticModel):

    name: str
    directories: list[Directory]
    files: list[File]
    


# class FileTree:
#     def __init__(self, directory, virtual_root):
#         self.Root = self.__create_tree(directory, virtual_root)

#     def __create_tree(self, dir: Path, virt_root, parent=None):
#         result = Directory(virt_root, parent=parent)
#         for f in dir.iterdir():
#             if f.is_file():
#                 result.files.append(File(f.name, parent=result))
#             elif f.is_dir():
#                 basename = os.path.basename(f.absolute())
#                 result.files.append(self.__createTree(
#                     f.absolute(), basename, result))
#         return result


class FileEncoder(JSONEncoder):
    def default(self, obj):
        res = obj.__dict__.copy()
        if "parent" in res.keys():
            if res["parent"] is None:
                res["parent"] = "none"
            else:
                res["parent"] = res["parent"].name
        return res


"""
        self.parent_directory = parent_directory
        self.is_directory=is_directory
        self.name = name
        self.downloaded_at = datetime.utcnow()
        if not is_directory:
            fullname = os.path.join(parent_directory,name)
            self.extension = os.path.splitext(name)[1]
            self.size = os.path.getsize(fullname)
"""
