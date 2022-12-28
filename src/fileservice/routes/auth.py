from fastapi import APIRouter, Depends, status

from ..models.user import User, UserCreate,Token
from ..services.auth import AuthService
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login")
def login(auth_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends()):
    print("Done")
    user = auth_service.authenticate_user(
        auth_data.username, auth_data.password)
    return auth_service.create_access_token(user)


@router.post("/refresh")
def refresh():
    pass


@router.post("/register",response_model=Token)
def register(create_request: UserCreate, auth_service: AuthService = Depends()):
    user = auth_service.create_user(create_request)
    return auth_service.create_access_token(user)


@router.post("/logout")
def logout():
    pass
