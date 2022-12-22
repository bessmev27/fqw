from datetime import datetime, timedelta
import os
from typing import Optional
from fastapi import Depends
from ..models.user import User, UserCreate, Token
from ..appsettings import AppSettings, get_settings
from ..database.repository.user import UserRepository
from .disk import DiskService
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class AuthService:
    def __init__(self, user_service: UserRepository = Depends(), app_settings: AppSettings = Depends(get_settings)):
        self.__user_service = user_service
        self.__pwd_context = CryptContext(
            schemes=["bcrypt"], deprecated="auto")
        self.__app_settings = app_settings

    def verify_token(self, token):
        payload = jwt.decode(
            token, self.__app_settings.jwt_secret, algorithms=[self.__app_settings.jwt_algorithm])
        user_data = payload.get("user")
        user = User.parse_obj(user_data)
        return user

    def get_password_hash(self, password):
        return self.__pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.__pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(self, username, password):
        user = self.__user_service.get_user(username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    def create_user(self, user_request):
        hashed_password = self.get_password_hash(user_request.password)
        data = user_request.dict()
        data.update({"hashed_password": hashed_password})
        return User.from_orm(self.__user_service.create_user(data))

    def create_access_token(self, user):
        user_data = User.from_orm(user)
        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=self.__app_settings.jwt_expires_s),
            'sub': str(user_data.id),
            'user': user_data.dict(),
        }
        token = jwt.encode(
            payload,
            self.__app_settings.jwt_secret,
            algorithm=self.__app_settings.jwt_algorithm,
        )
        return Token(access_token=token)


def get_current_user(token: str = Depends(oauth2_scheme), auth_service: AuthService = Depends()):
    return auth_service.verify_token(token)
