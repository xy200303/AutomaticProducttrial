from pydantic import BaseModel
from typing import Optional, Dict, Any
# 请求和响应模型
class Resp(BaseModel):
    code: int
    msg: str
    data: Any

    @classmethod
    def ok(cls, data, msg="请求成功"):
        return cls(
            code=200,
            msg=msg,
            data=data
        )

    @classmethod
    def err(cls, data, msg="请求失败"):
        return cls(
            code=400,
            msg=msg,
            data=data
        )

    @classmethod
    def resp(cls, code, data, msg=""):
        return cls(
            code=code,
            msg=msg,
            data=data
        )


class TryOnReq(BaseModel):
    person_img:str
    good_img:str

