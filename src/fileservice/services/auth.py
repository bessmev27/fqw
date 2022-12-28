from datetime import datetime, timedelta
import os
from typing import Optional
from fastapi import Depends
from ..models.user import User, UserCreate, Token
from ..appsettings import AppSettings, get_settings
from ..services.user import UserService
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from ..models.exception import NotAuthenticatedException, InvalidOperationException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class AuthService:
    def __init__(self, user_service: UserService = Depends(), app_settings: AppSettings = Depends(get_settings)):
        self.__user_service = user_service
        self.__pwd_context = CryptContext(
            schemes=["bcrypt"], deprecated="auto")
        self.__app_settings = app_settings

    def verify_token(self, token):
        try:
            payload = jwt.decode(
                token, self.__app_settings.jwt_secret, algorithms=[self.__app_settings.jwt_algorithm])
            user_data = payload.get("user")
            user = User.parse_obj(user_data)
            return user
        except JWTError as e:
            raise NotAuthenticatedException(
                "Invalid signature or token was expired") from e

    def get_password_hash(self, password):
        return self.__pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.__pwd_context.verify(plain_password, hashed_password)
    
    def create_user(self, user_request):
        user_request.password = self.get_password_hash(user_request.password)
        return self.__user_service.create_user(user_request)  

    def authenticate_user(self, username, password):
        exception = NotAuthenticatedException("Invalid username or password")
        user = self.__user_service.get_user(username)
        if not user:
            raise exception
        if not self.verify_password(password, user.password):
            return exception
        return user

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
