from fastapi import APIRouter

from . import (auth, disk, user)

router = APIRouter()
router.include_router(auth.router)
router.include_router(disk.router)
router.include_router(user.router)
