from __future__ import annotations
import datetime
from enum import Enum
from typing import Any, List, Literal, Optional, Tuple, Union

from pydantic import Field

from .base import BasePydanticModel

# BasePydanticModel - BaseModel


class FileType(str, Enum):
    DIRECTORY = "directory"
    FILE = "file"


class BaseFile(BasePydanticModel):
    id: int
    name: str
    created: datetime.datetime
    modified: Optional[datetime.datetime]
    parent_id: Optional[int]


class File(BaseFile):
    file_type: Literal[FileType.FILE] = FileType.FILE
    size: Optional[int]
    content_type: Optional[str]


class Directory(BaseFile):
    file_type: Literal[FileType.DIRECTORY] = FileType.DIRECTORY


class DirectoryWithChildren(Directory):
    children: List[Union[Directory, File]]

    # @classmethod
    # def from_db_model(cls, obj: Any) -> DirectorySchema:
    #     result = DirectorySchema.parse_obj(BaseFile.from_orm(obj).dict())
    #     if hasattr(obj,'children'):
    #         for child in obj.children:
    #             if child.file_type == FileType.FILE:
    #                 result.items.append(File.from_orm(child))
    #             elif child.file_type == FileType.DIRECTORY:
    #                 result.items.append(BaseFile.from_orm(child))
    #         print(result.items)
    #     return result


class FileDownloadResponse(BasePydanticModel):
    name: str
    path: str


class DirectoryCreateRequest(BasePydanticModel):
    parent_id: int
    name: str


class FileUpdateRequest(BasePydanticModel):
    name: str
    #parent_id: int


class DirectoryUpdateRequest(BasePydanticModel):
    name: str
    #parent_id: int


class FileUploadRequest(BasePydanticModel):
    parent_id: int
