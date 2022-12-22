from fastapi import FastAPI

from . import api

from .database.db import create_connection, create_if_not_exists
from .services.disk import DiskService
from .appsettings import AppSettings, get_settings
from .database.repository.file import FileRepository


create_if_not_exists()

db_session = next(create_connection())

file_repository = FileRepository(db_session)
file_service = DiskService(get_settings(), file_repository)
file_service.refresh()

del file_service
del db_session

app = FastAPI(
    title='File Service',
    description='Корпоративный сервис для файлового обмена',
    version='1.0.0',
)


app.include_router(api.router)
