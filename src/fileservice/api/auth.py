from fastapi import APIRouter, Depends, status

from ..services.disk import DiskService
from ..models.user import User, UserCreate
from ..services.auth import AuthService
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login")
def login(auth_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends()):
    user = auth_service.authenticate_user(
        auth_data.username, auth_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return auth_service.create_access_token(user)


@router.post("/refresh")
def refresh():
    pass


@router.post("/register")
def register(create_request: UserCreate, auth_service: AuthService = Depends(), disk_service: DiskService = Depends()):
    user = auth_service.create_user(create_request)
    disk_service.create_user_root(user.id)
    return auth_service.create_access_token(user)


@router.post("/logout")
def logout():
    pass
