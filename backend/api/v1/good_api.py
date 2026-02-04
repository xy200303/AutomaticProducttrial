import json
import os.path

from loguru import logger
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from backend.service.cache_service import get_cache_data, set_cache_data
from backend.service.good_service import get_good_data
from backend.utils import *
from backend.models import *
from backend.service import *
good_router = APIRouter()
@good_router.post("/get_item_data", response_model=Resp)
async def get_item_data(
    text:str
):
    good_data_resp=await get_good_data(text)
    return good_data_resp
    