import loguru
from pydantic import BaseModel
from typing import Optional, Dict, Any
from loguru import logger
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
    title:str

class GoodDataResp(BaseModel):
    item_imgs:list
    prop_imgs:list
    title:str
    price:float

    @classmethod
    def from_onebound_tb_good_data(cls,tb_good_data):
        logger.debug(f"tb_good_data: {tb_good_data}")
        error_code=tb_good_data.get("error_code",None)
        if error_code=="0000":
            item=tb_good_data.get("item",{})
            item_imgs=item.get("item_imgs",[])
            props_img=item.get("props_img",{})
            if len(item_imgs)==0:
                return Resp.err(data=tb_good_data["error"],msg=str(tb_good_data["reason"]))
            else:
                item_imgs=["https:"+img["url"] for img in item_imgs if img.get("url",None) is not None]
                prop_imgs=[v for k,v in props_img.items() if v is not None]
                title=item["title"]
                price=item["price"]
                return Resp.ok(data=cls(
                    title=title,
                    price=price,
                    item_imgs=item_imgs,
                    prop_imgs=prop_imgs
                ),msg=str(tb_good_data["reason"]))
        else:
            return Resp.err(data=tb_good_data["error"],msg=str(tb_good_data["reason"]))

    @classmethod
    def from_onebound_jd_good_data(cls,jd_good_data):
        logger.debug(f"jd_good_data: {jd_good_data}")
        error_code = jd_good_data.get("error_code", None)
        if error_code == "0000":
            item = jd_good_data.get("item", {})
            item_imgs = item.get("item_imgs", {}).get("item_img",[])
            props_img = item.get("props_img", [])

            if len(item_imgs) == 0:
                return Resp.err(data=jd_good_data["error"], msg=str(jd_good_data["reason"]))
            else:
                item_imgs = ["https:"+img["url"] for img in item_imgs if img.get("url", None) is not None]
                logger.debug(f"jd_item_imgs: {item_imgs}")
                logger.debug(f"jd_props_img: {props_img}")
                prop_imgs = ["https:"+v for prop in props_img for k,v in prop.items() if v is not None]

                title = item["title"]
                price = item["price"]
                return Resp.ok(data=cls(
                    title=title,
                    price=price,
                    item_imgs=item_imgs,
                    prop_imgs=prop_imgs
                ), msg=str(jd_good_data["reason"]))
        else:
            return Resp.err(data=jd_good_data["error"], msg=str(jd_good_data["reason"]))
