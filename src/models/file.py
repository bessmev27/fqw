from .base import BasePydanticModel

from .directory import Directory

class File(BasePydanticModel):

    name: str
    size: int
    directory: Directory
   