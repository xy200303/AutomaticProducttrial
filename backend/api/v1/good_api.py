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
    item_data=await get_good_data(text)
    if item_data is None:
        return Resp.err(None)
    if item_data is not None and item_data["code"]==0:
        return Resp.ok(item_data["data"])
    else:
        return Resp.err(item_data["data"],msg=str(item_data["message"]))
    