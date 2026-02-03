
from fastapi import APIRouter, HTTPException
from .good_api import good_router
from .upload_api import upload_router
from .image_api import image_router
v1_router = APIRouter()
v1_router.include_router(good_router, tags=["good"])
v1_router.include_router(upload_router, tags=["upload"])
v1_router.include_router(image_router, tags=["image"])
