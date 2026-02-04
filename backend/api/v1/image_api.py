import json
import os.path

from loguru import logger
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from backend.service.cache_service import get_cache_data, set_cache_data
from backend.service.good_service import get_good_data
from backend.service.image_service import dashscope_try_on, title_2_type
from backend.utils import *
from backend.models import *
from backend.service import *

image_router = APIRouter()


@image_router.post("/try_on", response_model=Resp)
async def try_on(
    data:TryOnReq
):
    if data.good_img is None or data.good_img== "":
        return Resp.err(data=None,msg="参数商品文本链接为空")
    if data.person_img is None or data.person_img== "":
        return Resp.err(data=None, msg="参数人物图像为空")
    response=await dashscope_try_on(
        type=title_2_type(data.title),
        good_img=data.good_img,
        person_img=data.person_img,
    )
    if response.status_code == 200:
        # 如需查看完整响应，请取消下行注释
        # print(json.dumps(response, ensure_ascii=False))
        img_url_list=[]
        for i, content in enumerate(response.output.choices[0].message.content):
            img_url=content['image']
            img_url_list.append(img_url)
        return Resp.ok(data=img_url_list)
    else:
        return Resp.err(
            data=None,
            msg=response.message,
        )

