from fastapi import APIRouter, HTTPException
from loguru import logger

# 创建一个测试路由来验证全局异常处理
exception_test_router = APIRouter()

@exception_test_router.get("/test/http-exception")
async def test_http_exception():
    """测试HTTP异常处理"""
    raise HTTPException(status_code=400, detail="这是一个测试HTTP异常")

@exception_test_router.get("/test/value-error")
async def test_value_error():
    """测试值错误异常处理"""
    raise ValueError("这是一个测试值错误")

@exception_test_router.get("/test/permission-error")
async def test_permission_error():
    """测试权限错误异常处理"""
    raise PermissionError("这是一个测试权限错误")

@exception_test_router.get("/test/file-not-found")
async def test_file_not_found():
    """测试文件未找到异常处理"""
    raise FileNotFoundError("这是一个测试文件未找到错误")

@exception_test_router.get("/test/general-exception")
async def test_general_exception():
    """测试通用异常处理"""
    raise Exception("这是一个测试通用异常")

@exception_test_router.get("/test/success")
async def test_success():
    """测试正常响应"""
    return {"message": "请求成功", "status": "ok"}