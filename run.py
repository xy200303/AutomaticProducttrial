import loguru
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
import os
from contextlib import asynccontextmanager

from starlette.staticfiles import StaticFiles

# 导入配置模块
from backend.config import Config
from backend.utils import *
from backend.api import api_router
from backend.middleware.exception_handler import GlobalExceptionMiddleware
# 创建FastAPI应用实例

# 应用启动事件
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用启动时的初始化操作"""
    try:
        # 加载配置文件
        os.makedirs("./static",exist_ok=True)
        os.makedirs("./upload",exist_ok=True)
        os.makedirs("./temp",exist_ok=True)
        os.makedirs("./cache",exist_ok=True)
        print("✅ 应用配置加载成功")
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        # 不阻止应用启动，但在需要配置的地方会报错
    yield
app = FastAPI(
    title="自动商品试用 API",
    description="自动商品试用系统的后端API服务",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该配置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置全局异常处理中间件
app.add_middleware(GlobalExceptionMiddleware)
app.mount("/upload", StaticFiles(directory="./upload"), name="upload")
# 挂载前端构建产物
if os.path.exists("web/dist"):
    app.mount("/assets", StaticFiles(directory="web/dist/assets"), name="assets")

app.include_router(api_router, prefix="/api", tags=["api"])




# 基础路由
@app.get("/")
async def root():
    """根路径，返回前端页面"""
    if os.path.exists("web/dist/index.html"):
        return FileResponse("web/dist/index.html")
    return {
        "message": "自动商品试用 API 服务已启动 (前端页面未构建)",
        "version": "1.0.0",
        "docs": "/docs"
    }


# 主函数，用于直接运行应用
if __name__ == "__main__":
    # 获取端口，默认8000
    port = int(os.getenv("PORT", 8000))
    # 运行应用
    uvicorn.run(
        "run:app",
        host="0.0.0.0",
        port=port,
        reload=True,  # 开发模式下启用热重载
        log_level="info"
    )