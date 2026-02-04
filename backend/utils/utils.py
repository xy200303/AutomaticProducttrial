import asyncio
import hashlib

import aiohttp
import requests

import base64
import time
import rsa
from backend.config import Config
from loguru import logger
def generate_rsa_password(domain="www.sojson.com"):
    """
    生成 RSA 加密密码
    返回格式: {'raw': '原始数据', 'encrypted': '加密密码'}
    """
    # 预设公钥
    PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCM2eQ5SNpL7Lbv9Uh6UPY/kk5H
    pm1fwjPriMd2n3aACGQKus3L3xYnsd67BThXFh7+khiTZ0Ixm9HX03EbS8N6ogge
    oordvWN6oIS75RRhJFqHZhCdf18W27FmOoBp5tlQXPt0z7tdi3KG4D+4464tsbyy
    bvESDCG3yWVeK0HB9wIDAQAB
    -----END PUBLIC KEY-----"""
    # 生成原始数据
    timestamp = str(int(time.time() * 1000))
    raw_data = f"{domain}|{timestamp}"
    
    # RSA 加密
    pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(PUBLIC_KEY.encode())
    encrypted = rsa.encrypt(raw_data.encode(), pub_key)
    encrypted_b64 = base64.b64encode(encrypted).decode()
    return {'raw': raw_data, 'encrypted': encrypted_b64}

async def parse_short_url(short_url):
    """
    解析淘宝短链接
    返回格式: {'item_id': '商品ID', 'short_url': '短链接'}
    """
    cookies = {
        'UM_distinctid': '19c1eca0b47581-094fc4889ca63d8-4c657b58-144000-19c1eca0b48a8b',
        'Hm_lvt_7fdddaba98edbe9661b96c5daae1f97e': '1770043084',
        'HMACCOUNT': 'E42372FC73EA671D',
        '_gid': 'GA1.2.456681068.1770043084',
        'CNZZDATA1281461823': '880579740-1770043084-https%253A%252F%252Fcn.bing.com%252F%7C1770043795',
        'Hm_lpvt_7fdddaba98edbe9661b96c5daae1f97e': '1770043795',
        '_gat_gtag_UA_114686494_1': '1',
        '_ga': 'GA1.1.1205595229.1770043084',
        '__gads': 'ID=f0c9946af74252b6:T=1770043084:RT=1770043795:S=ALNI_MZXgDnIGHlrJyVGVL_AmV83vvjdXg',
        '__gpi': 'UID=000011f102b29975:T=1770043084:RT=1770043795:S=ALNI_MYLLdP0q6ywH9Ng_f6TSIsXOe1fxQ',
        '__eoi': 'ID=29a9e079b7769e0a:T=1770043084:RT=1770043795:S=AA-AfjZtVfcp8z92niYfFoFzPKnO',
        '_ga_4RSL38R3BR': 'GS2.1.s1770043083$o1$g1$t1770043797$j58$l0$h0',
        '_ga_CW21F2LYW8': 'GS2.1.s1770043083$o1$g1$t1770043802$j53$l0$h0',
    }

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.sojson.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.sojson.com/dwz/parse.html',
        'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Microsoft Edge";v="144"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sojsonhost': generate_rsa_password()['encrypted'],
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0',
        'x-requested-with': 'XMLHttpRequest',
        # 'cookie': 'UM_distinctid=19c1eca0b47581-094fc4889ca63d8-4c657b58-144000-19c1eca0b48a8b; Hm_lvt_7fdddaba98edbe9661b96c5daae1f97e=1770043084; HMACCOUNT=E42372FC73EA671D; _gid=GA1.2.456681068.1770043084; CNZZDATA1281461823=880579740-1770043084-https%253A%252F%252Fcn.bing.com%252F%7C1770043795; Hm_lpvt_7fdddaba98edbe9661b96c5daae1f97e=1770043795; _gat_gtag_UA_114686494_1=1; _ga=GA1.1.1205595229.1770043084; __gads=ID=f0c9946af74252b6:T=1770043084:RT=1770043795:S=ALNI_MZXgDnIGHlrJyVGVL_AmV83vvjdXg; __gpi=UID=000011f102b29975:T=1770043084:RT=1770043795:S=ALNI_MYLLdP0q6ywH9Ng_f6TSIsXOe1fxQ; __eoi=ID=29a9e079b7769e0a:T=1770043084:RT=1770043795:S=AA-AfjZtVfcp8z92niYfFoFzPKnO; _ga_4RSL38R3BR=GS2.1.s1770043083$o1$g1$t1770043797$j58$l0$h0; _ga_CW21F2LYW8=GS2.1.s1770043083$o1$g1$t1770043802$j53$l0$h0',
    }

    data = {
        'url': short_url,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post('https://www.sojson.com/auth_v_1_0/http/dwz-decode.shtml', headers=headers,cookies=cookies,data=data,ssl=False) as response:
                # 检查 HTTP 状态码，如 4xx / 5xx 会触发异常
                response.raise_for_status()
                # 解析返回的 JSON 数据
                data = await response.json()
                if "url" not in data:
                    logger.error(f"解析短链{short_url}出错{data}")
                    return None
                return data['url']
    except aiohttp.ClientResponseError as e:
        logger.error(e)
        raise e

from urllib.parse import urlparse, parse_qs

def extract_tb_item_id(url):
    """
    从 URL 中提取 id 参数
    
    Args:
        url (str): 要解析的 URL
        
    Returns:
        str or None: 提取到的 id 值，如果不存在则返回 None
    """
    try:
        # 解析 URL
        parsed_url = urlparse(url)
        # 解析查询参数
        query_params = parse_qs(parsed_url.query)
        # 获取 id 参数（parse_qs 返回列表，取第一个元素）
        if 'id' in query_params and query_params['id']:
            return query_params['id'][0]
        elif "itemIds" in query_params and query_params['itemIds']:
            return query_params['itemIds'][0]
        return None
    except Exception as e:
        print(f"URL 解析错误: {e}")
        return None

async def get_taobao_item_justone(item_id: str):
    if Config.just_one_api_key is None or Config.just_one_api_key == '':
        raise Exception("请先配置JustOneAPI接口")
    url = f"http://47.117.133.51:30015/api/taobao/get-item-detail/v5?token={Config.just_one_api_key}&itemId={item_id}"
    headers = {}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                # 检查 HTTP 状态码，如 4xx / 5xx 会触发异常
                response.raise_for_status()
                # 解析返回的 JSON 数据
                data = await response.json()
                print(data)
                return data
    except aiohttp.ClientResponseError as e:
        logger.error(e)
        raise e

async def get_taobao_item_onebound(item_id: str):
    if Config.onebound_api_key is None or Config.onebound_api_key == '':
        raise Exception("请先配置万邦API接口")
    url = f"https://api-gw.onebound.cn/taobao/item_get/?key={Config.onebound_api_key}&num_iid={item_id}&lang=zh-CN&secret={Config.onebound_api_secret}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                # 检查 HTTP 状态码，如 4xx / 5xx 会触发异常
                response.raise_for_status()
                # 解析返回的 JSON 数据
                data = await response.json()
                return data
    except aiohttp.ClientResponseError as e:
        logger.error(e)
        raise e

async def get_jd_item_justone(item_id: str):
    if Config.just_one_api_key is None or Config.just_one_api_key == '':
        raise Exception("请先配置JustOneAPI接口")
    url = f"http://47.117.133.51:30015/api/jd/get-item-detail/v1?token={Config.just_one_api_key}&itemId={item_id}"
    headers = {}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                # 检查 HTTP 状态码，如 4xx / 5xx 会触发异常
                response.raise_for_status()
                # 解析返回的 JSON 数据
                data = await response.json()
                return data
    except aiohttp.ClientResponseError as e:
        logger.error(e)
        raise e


async def get_jd_item_onebound(item_id: str):
    if Config.onebound_api_key is None or Config.onebound_api_key == '':
        raise Exception("请先配置万邦API接口")
    url = f"https://api-gw.onebound.cn/jd/item_get_pro/?key={Config.onebound_api_key}&num_iid={item_id}&lang=zh-CN&secret={Config.onebound_api_secret}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                # 检查 HTTP 状态码，如 4xx / 5xx 会触发异常
                response.raise_for_status()
                # 解析返回的 JSON 数据
                data = await response.json()
                return data
    except aiohttp.ClientResponseError as e:
        logger.error(e)
        raise e


import re
extract_url_from_text = lambda text: re.search(r'https?://[^\s]+', text).group().strip() if re.search(r'https?://[^\s]+', text) else None
def extract_jd_item_id(url):
    # 匹配类似 https://item.jd.com/100076891945.html 的 URL
    match = re.search(r'.jd\.com/(\d+)\.html', url)
    if match:
        return match.group(1)  # 返回 100076891945
    else:
        match = re.search(r'.jd\.com/product/(\d+)\.html', url)
        if match:
            return match.group(1)  # 返回 100076891945
        else:
            return None  # 如果没有匹配到，返回 None


def hash(data):
    """计算数据的 MD5 哈希值"""
    m = hashlib.md5()
    # 处理不同类型的数据
    if isinstance(data, str):
        # 如果是字符串，需要先编码为 bytes
        m.update(data.encode('utf-8'))
    elif isinstance(data, bytes):
        # 如果已经是 bytes，直接使用
        m.update(data)
    else:
        # 其他类型转换为字符串再编码
        m.update(str(data).encode('utf-8'))
    return m.hexdigest()


# print(extract_jd_item_id("https://cfe.m.jd.com/privatedomain/risk_handler/03101900/?returnurl=https://item.m.jd.com/product/10198442068639.html?gx=RnAomTM2bzHZzZkV-o1_CxJqklyq4DA&gxd=RnAoxm4LamKIzZEV_tJ_WxaOPBUahPA&ad_od=share&utm_source=androidapp&utm_medium=appshare&utm_campaign=t_335139774&utm_term=CopyURL_shareid59b2fa690af86672177010249648868712_shangxiang_none&jkl=@RB0Rr0ES1b@&appid=2146&evtype=3&evurl=https://cfe.m.jd.com/privatedomain/risk_handler/03101900/&rpid=rp-190153108-10283-1770102523007"))

# print(extract_taobao_item_id("https://detail.tmall.com/item.htm?ali_refid=a3_430673_1006%3A1572350051%3AH%3Ah0rcYa9C4Mh89FvEWMZiaw%3D%3D%3A22d1212874851602bc243857d39a6b25&ali_trackid=318_22d1212874851602bc243857d39a6b25&id=757910328369&loginBonus=1&mi_id=0000WV821VV2U9nL3mv7iHskDH4qLhrPPOzbuYvOwW02dyk&mm_sceneid=0_0_2169130052_0&priceTId=215042c317701030116771456e156e&skuId=5225546068752&spm=a21n57.sem.item.2&utparam=%7B%22aplus_abtest%22%3A%22377c1e29413c91a9e6d597f5bdce3a74%22%7D&xxc=ad_ztc"))

# get_jd_item("10069391687670")
