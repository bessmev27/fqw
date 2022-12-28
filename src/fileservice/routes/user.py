from fastapi import APIRouter, Depends, status

from ..services.user import UserService
from ..services.disk import DiskService
from ..models.user import User, UserCreate


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/")
def get_users(user_service: UserService = Depends()):
    return user_service.get_users()


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(request: UserCreate, user_service: UserService = Depends(), disk_service: DiskService = Depends()):
    new_user = user_service.create_user(request)
    return new_user
