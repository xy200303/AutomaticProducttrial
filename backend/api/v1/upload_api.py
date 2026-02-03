import json
import os.path

from loguru import logger
from fastapi import APIRouter, HTTPException, UploadFile
from pydantic import BaseModel
from typing import List, Optional
from fastapi import UploadFile, File, HTTPException, Depends, status
from backend.service.cache_service import get_cache_data, set_cache_data
from backend.utils import *
from backend.models import *
from backend.service import *

upload_router = APIRouter()

ALLOWED_FILE_TYPES=["image/jpeg", "image/png", "image/webp", "image/jpg"]

@upload_router.post("/upload_file", response_model=Resp)
async def upload_file(
    file: UploadFile = File(..., description="上传一个图片文件")
):
    """
        上传单个图片文件
        - 限制文件类型为 jpg/jpeg/png/webp
        - 重命名文件避免冲突
        - 返回访问 URL
        """
    # 1. 校验文件类型
    if file.content_type not in ALLOWED_FILE_TYPES:
        return Resp.err(
            data=None,
            msg="不支持的文件类型"
        )
    try:
        # 2. 初始化哈希计算器
        sha256_hash = hashlib.sha256()
        # 3. 分块读取文件并更新哈希（避免大文件内存溢出）
        contents = await file.read()
        sha256_hash.update(contents)
        # 4. 获取十六进制哈希值
        file_hash = sha256_hash.hexdigest()
        # 5. 可选：使用 hash 作为文件名一部分（增强唯一性 & 去重）
        # 方式1：纯 UUID（当前做法）
        # filename = f"{uuid.uuid4().hex}.{ext}"
        # 方式2：使用 hash 作为文件名（推荐用于去重）
        filename = f"{file_hash}.png"
        file_path = os.path.join("./upload", filename)
        file_url = f"/upload/{filename}"
        # 6. 如果文件已存在（去重逻辑）
        if os.path.exists(file_path):
            return Resp.ok(
                data={
                    "path": file_url,
                    "url": file_url,
                    "file_id": file_hash,
                },
                msg="文件已经存在"
            )
        # 7. 保存文件
        with open(file_path, "wb") as f:
            f.write(contents)
        return Resp.ok(
            data={
                "path": file_url,
                "url": file_url,
                "file_id": file_hash,
            },
            msg="上传成功"
        )
    except Exception as e:
        return Resp.err(
            data=None,
            msg=str(e)
        )
    finally:
        await file.close()
