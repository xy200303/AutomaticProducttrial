import asyncio
import json
import os
from dashscope import MultiModalConversation
import base64
import mimetypes
import dashscope

from backend.config import Config
# 以下为中国（北京）地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

# ---用于 Base64 编码 ---
# 格式为 data:{mime_type};base64,{base64_data}
def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("不支持或无法识别的图像格式")
    try:
        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(
                image_file.read()).decode('utf-8')
        return f"data:{mime_type};base64,{encoded_string}"
    except IOError as e:
        raise IOError(f"读取文件时出错: {file_path}, 错误: {str(e)}")
from functools import partial

async def dashscope_image_edit(
    messages
):
    def sync_call(m):
        # qwen-image-edit-max、qwen-image-edit-plus系列支持输出1-6张图片，此处以2张为例
        response = MultiModalConversation.call(
            api_key=Config.dashscope_api_key,
            model="qwen-image-edit-max-2026-01-16",
            messages=m,
            stream=False,
            n=1,
            watermark=False,
            negative_prompt=" ",
            prompt_extend=True,
            size="1536*1024",
        )
        return response
    bound_sync_call = partial(sync_call, m=messages)
    response = await asyncio.to_thread(bound_sync_call)
    return response

#试穿衣服
async def dashscope_try_on(good_img,person_img,pose_img=None,type=None):
    content=[{
        "image": person_img,
    },
        {
            "image": good_img,
        }]
    if pose_img is not None:
        content.append({
            "image": pose_img,
        })
    if type=="cloth":
        prompt = f"""
        图1为一位普通用户的图像，包含其原始背景、姿态、表情和穿着；图2是一件衣服的商品图像（需忽略其背景，仅提取衣服本身）。  
        请将图2中的衣服穿到图1的人物身上，替换其原有上衣或外衣，保持衣服的样式、颜色、图案和材质完全不变，并确保衣服合身、自然贴合身体，呈现真实的穿着效果。  

        关键要求如下：  
        - 严格保留图1中人物的原始背景、姿态、表情和身材比例，仅更换衣服部分；  
        - 衣服与人物身体自然融合，有合理的褶皱、垂感和阴影，避免漂浮、变形或边缘不贴合；  
        - 忽略衣服图像的原始背景，仅使用衣服主体进行合成；  
        - 光线应与原始图像一致（如室内灯、自然光等），保持整体光影协调；  
        - 人物表情自然、生活化，画面风格贴近真实用户日常穿着拍摄（如自拍、镜子前拍照、街拍等），避免商业广告感；  
        - 输出高清画质，全身或半身视角均可，但需完整展示衣服上身效果；  
        - 整体效果应真实、自然、接地气，接近“买家秀”或真实用户分享的照片。
        """
    elif type=="hat":
        prompt = f"""
        图1为某个人物的图像，包含其原始背景、姿态和表情；图2是帽子或围巾类商品的图像。  
        请将图2中的商品自然地戴到人物身上（帽子戴在头上，围巾围在颈部），确保商品的样式、颜色、纹理和图案完全保持不变。  

        具体要求如下：  
        - 严格保留图1中人物的原始背景、姿态、表情和身材比例，仅添加或更换目标配饰；  
        - 商品需与人物身体部位自然贴合（如帽子贴合头型、围巾自然环绕颈部），比例协调，无违和感；  
        - 细节丰富，材质与色彩真实还原，光影过渡自然，与原始图像的光线环境一致（如室内光、自然光）；  
        - 避免出现商品漂浮、变形、位置错误或边缘不贴合等问题；  
        - 图像清晰，可采用全身或半身视角，完整展示佩戴效果；  
        - 整体风格贴近真实用户日常佩戴场景（如自拍、出门前照镜、冬季街拍等），光线自然，无商业影棚感，接近“买家秀”或生活记录照片效果。
        """
    elif type=="shoe":
        prompt = f"""
        图1为某个人物的图像，包含其原始背景、姿态、表情和脚部状态；图2是鞋类或袜子类商品的图像。  
        请将图2中的商品自然地穿到人物的脚上（鞋子穿在脚上，袜子穿在脚上或鞋内），确保商品的样式、颜色、纹理和图案完全保持不变。  

        具体要求如下：  
        - 严格保留图1中人物的原始背景、姿态、表情和身材比例，仅更换或添加脚部穿戴商品；  
        - 商品需与脚部自然贴合，比例协调，无违和感（如鞋子包裹脚型、袜子平整无褶皱堆积）；  
        - 忽略商品图像的原始背景，仅提取商品主体进行融合；  
        - 细节丰富，材质与色彩真实还原，光影过渡自然，与原始图像的光线环境保持一致（如室内光、自然光、街拍光）；  
        - 避免出现商品漂浮、变形、位置错误或边缘不贴合等问题；  
        - 图像清晰高分辨率，建议采用全身或半身视角，完整展示脚部穿戴效果；  
        - 整体风格贴近真实用户日常穿着场景（如自拍、出门前、试鞋间、街头行走等），光线自然，无商业影棚打光感，接近“买家秀”或生活记录照片效果。
        """
    else:
        prompt = f"""
        图1为一位普通用户的图像，包含其原始背景、姿态、表情和身材；图2是目标商品图像（可为鞋类、袜子、衣服、首饰、帽子、围巾等）。  
        请将该商品自然地穿到、戴到或配备到人物身上，确保商品的样式、颜色、纹理、图案完全保持不变。  
        商品原有背景无需保留，仅提取商品主体进行融合处理。  

        要求如下：  
        - 严格保留图1中人物的原始背景、姿态、表情和身材比例，仅更换或添加目标商品；  
        - 商品需与人物身体部位（如脚、手、头部、颈部等）自然贴合，比例协调，无违和感；  
        - 细节丰富，材质与色彩真实还原，光影过渡自然，与原始图像的光线环境保持一致（如室内灯、窗边自然光、阴天户外光等）；  
        - 图像清晰高分辨率，采用全身照或半身照视角，完整展示商品上身/下身效果；  
        - 避免商品漂浮、变形、位置错误或边缘不贴合等问题；  
        - 整体画面风格贴近真实用户日常生活穿着场景（如自拍、镜子前、试衣间、街头等），光线自然，无商业影棚感；  
        - 保持人物姿态自然放松，画面和谐统一，接近用户实拍“买家秀”或生活记录照片效果，而非广告大片。
        """
    content.append({
        "text" :prompt,
    })
    messages = [
        {
            "role": "user",
            "content": content
        }
    ]
    return await dashscope_image_edit(messages)

