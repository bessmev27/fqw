#from datetime import datetime
from json import JSONEncoder
from sqlalchemy import Boolean, Column, DateTime,String,Integer,ForeignKey, func
from sqlalchemy.orm import relationship,backref

from .base import Base,Base

class Directory(Base):

    __tablename__ = "user_directories"

    id = Column(Integer,primary_key=True)
    name = Column(String)
    parent_id = Column(Integer,ForeignKey("user_directories.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    directories = relationship("Directory", backref=backref("parent", remote_side=[id]))
    files = relationship("File",back_populates="directory")
    created_utc = Column(DateTime(timezone=True), server_default=func.now())
    is_deleted = Column(Boolean)
    last_updated_by = Column(Integer)
    last_updated_utc = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self) -> str:
        return f"parent_id = {self.parent_id} ; name = {self.name}"


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
