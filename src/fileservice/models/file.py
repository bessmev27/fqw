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
    modified: datetime.datetime
    parent_id: Optional[int]


class File(BaseFile):
    file_type: Literal[FileType.FILE] = FileType.FILE
    size: int
    content_type: str


class Directory(BaseFile):
    file_type: Literal[FileType.DIRECTORY] = FileType.DIRECTORY


class DirectoryWithChildren(Directory):
    children: List[Union[Directory, File]]


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
    name: str
    size: int
    content_type: str
    key: str
