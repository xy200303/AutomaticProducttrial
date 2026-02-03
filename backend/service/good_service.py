from backend.service.cache_service import *
from backend.utils import *
from loguru import logger

#解析短链
async def get_url_by_short_url(url):
    key=hash(url)
    url_data=get_cache_data(f"url_{key}")
    if url_data is not None:
        return url_data['url']
    else:
        url=await parse_short_url(url)
        if url is not None:
            set_cache_data(f"url_{key}", {
                "url": url,
            })
    return url
#从文本提取商品
async def get_good_data(
    text:str
):
    item_data = None
    url = extract_url_from_text(text)
    if ("jd.com" not in url) and ("tmall.com" not in url) and ("taobao.com" not in url):
        url = await get_url_by_short_url(url)
    if url is None:
        return None
    if "jd.com" in url:
        item_id = extract_jd_item_id(url)
        item_data = get_cache_data(f"jd_{item_id}")
        if item_data is None:
            logger.info(f"jd {item_id}数据文件不存在")
            item_data = await get_jd_item(item_id)
            if item_data is not None and item_data["code"] == 0:
                set_cache_data(f"jd_{item_id}", item_data)
    if ("tmall.com" in url) or ("taobao.com" in url):
        item_id = extract_tb_item_id(url)
        item_data = get_cache_data(f"tb_{item_id}")
        if item_data is None:
            logger.info(f"tb {item_id}数据文件不存在")
            item_data = await get_taobao_item(item_id)
            if item_data is not None and item_data["code"] == 0:
                set_cache_data(f"tb_{item_id}", item_data)
    return item_data