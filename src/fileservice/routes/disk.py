from typing import List, Optional, Union
from fastapi import APIRouter, Depends, UploadFile, HTTPException, status, Response
from ..services.auth import get_current_user
from ..services.disk import DiskService
from ..models.user import User
from ..models.file import *
from fastapi.responses import FileResponse


router = APIRouter(
    prefix='/disk',
    tags=['disk']
)


@router.get('/', response_model=DirectoryWithChildren)
def get_directory_root(user: User = Depends(get_current_user), disk_service: DiskService = Depends()):
    result = disk_service.get_user_root(user.id)
    return result


@router.get("/directories/{directory_id}", response_model=DirectoryWithChildren)
def get_directory(directory_id: int, user: User = Depends(get_current_user), disk_service: DiskService = Depends()):
    result = disk_service.get_directory(user.id, directory_id)
    return result


@router.post('/directories', response_model=Directory, status_code=status.HTTP_201_CREATED)
def create_directory(request: DirectoryCreateRequest, user: User = Depends(get_current_user),
                     disk_service: DiskService = Depends()):
    return disk_service.create_directory(user.id, request)


@router.delete("/directories/{directory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_directory(directory_id: int, user: User = Depends(get_current_user), disk_service: DiskService = Depends()):
    disk_service.delete_directory(user.id, directory_id)


@router.delete("/files/{file_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Deletes a file")
def delete_file(file_id: int, user: User = Depends(get_current_user), disk_service: DiskService = Depends()):
    disk_service.delete_file(user.id, file_id)


@router.post('/upload', response_model=List[File], status_code=status.HTTP_201_CREATED)
def upload_file(files: List[UploadFile], parent_id: int, user: User = Depends(get_current_user), disk_service: DiskService = Depends()):
    result = disk_service.upload_file(user.id, parent_id, files)
    return result


@router.patch("/files/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def rename_file(request: FileUpdateRequest, file_id: int, user: User = Depends(get_current_user), disk_service: DiskService = Depends()):
    return disk_service.rename_file(user.id, file_id, request)


@router.patch("/directories/{directory_id}", status_code=status.HTTP_204_NO_CONTENT)
def rename_directory(request: DirectoryUpdateRequest, directory_id: int, user: User = Depends(get_current_user), disk_service: DiskService = Depends()):
    return disk_service.rename_directory(user.id, directory_id, request)


@router.patch("/directories/{directory_id}/{deleted_status}", status_code=status.HTTP_204_NO_CONTENT)
def set_status_directory(response: Response, directory_id: int, deleted_status: bool, user: User = Depends(get_current_user), disk_service: DiskService = Depends()):
    disk_service.set_status_directory(user.id, directory_id, deleted_status)


@router.patch("/files/{file_id}/{deleted_status}", status_code=status.HTTP_204_NO_CONTENT)
def set_status_file(response: Response, file_id: int, deleted_status: bool, user: User = Depends(get_current_user), disk_service: DiskService = Depends()):
    disk_service.set_status_file(user.id, file_id, deleted_status)


# need to move this method to download service
@router.get('/download/{file_id}')
def download_file(file_id: int, user: User = Depends(get_current_user), disk_service: DiskService = Depends()):
    response = disk_service.download_file(user.id, file_id)
    return FileResponse(path=response.path, filename=response.name)
