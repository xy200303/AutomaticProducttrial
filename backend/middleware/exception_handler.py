import traceback
from typing import Any, Optional
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from backend.models import Resp
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class GlobalExceptionMiddleware(BaseHTTPMiddleware):
    """
    全局异常处理中间件
    捕获所有未处理的异常并返回统一的错误响应格式
    """
    
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException as http_exc:
            # 处理HTTP异常
            logger.warning(f"HTTP异常: {http_exc.detail} - 路径: {request.url.path}")
            return JSONResponse(
                status_code=http_exc.status_code,
                content=Resp.err(
                    data=None,
                    msg=http_exc.detail or "请求失败"
                ).dict()
            )
        except ValueError as ve:
            # 处理值错误
            logger.error(f"值错误异常: {str(ve)} - 路径: {request.url.path}")
            return JSONResponse(
                status_code=400,
                content=Resp.err(
                    data=None,
                    msg=f"参数错误: {str(ve)}"
                ).dict()
            )
        except PermissionError as pe:
            # 处理权限错误
            logger.error(f"权限错误: {str(pe)} - 路径: {request.url.path}")
            return JSONResponse(
                status_code=403,
                content=Resp.err(
                    data=None,
                    msg="权限不足"
                ).dict()
            )
        except FileNotFoundError as fe:
            # 处理文件未找到错误
            logger.error(f"文件未找到: {str(fe)} - 路径: {request.url.path}")
            return JSONResponse(
                status_code=404,
                content=Resp.err(
                    data=None,
                    msg="资源不存在"
                ).dict()
            )
        except Exception as exc:
            # 处理所有其他未预期的异常
            logger.error(f"未预期的异常: {str(exc)} - 路径: {request.url.path}")
            logger.error(f"异常堆栈: {traceback.format_exc()}")
            
            # 在生产环境中，不要暴露详细的错误信息给客户端
            error_msg = "服务器内部错误"
            
            return JSONResponse(
                status_code=500,
                content=Resp.err(
                    data=None,
                    msg=error_msg
                ).dict()
            )