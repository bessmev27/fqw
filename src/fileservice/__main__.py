from multiprocessing import freeze_support
import uvicorn
from .appsettings import get_settings
import os

settings = get_settings()


uvicorn.run(
    'fileservice.app:app',
    reload=True,
    host=settings.server_host,
    port=settings.server_port
)
