from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from .v1 import v1_router
api_router = APIRouter()

api_router.include_router(v1_router, tags=["v1"])