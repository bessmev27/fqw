from fastapi import FastAPI

from . import routes

from .database.db import create_connection, create_if_not_exists
from .services.disk import DiskService
from .appsettings import AppSettings, get_settings
from .database.repository.file import FileRepository
from .models.exception import InvalidOperationException, NotAuthenticatedException,UnexpectedException
from fastapi.responses import Response, JSONResponse
from fastapi import status, HTTPException
from fastapi.exception_handlers import http_exception_handler

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

app.include_router(routes.router)


@app.exception_handler(ValueError)
async def invalid_data_exception_handler(request, exc):
    exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return await http_exception_handler(request, exception)


@app.exception_handler(InvalidOperationException)
async def invalid_operation_exception_handler(request, exc):
    exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return await http_exception_handler(request, exception)


@app.exception_handler(NotAuthenticatedException)
async def not_authenticated_exception_handler(request, exc):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=str(exc),
        headers={'WWW-Authenticate': 'Bearer'},
    )
    return await http_exception_handler(request, exception)

@app.exception_handler(UnexpectedException)
async def unexpected_exception_handler(request, exc):
    exception = HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
    return await http_exception_handler(request, exception)