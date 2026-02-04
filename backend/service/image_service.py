import asyncio
import json
import os
from dashscope import MultiModalConversation
import base64
import mimetypes
import dashscope
from loguru import logger
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

def title_2_type(title):
    """
    根据标题中的关键词判断商品类型
    :param title: 商品标题字符串
    :return: 商品类型字符串，如 'cloth', 'shoe' 等，未匹配返回 None
    """
    # 定义分类与关键词映射表（可轻松扩展）
    category_keywords = {
        "cloth": ['裤', '衣', '外套', '衬衫', 'T恤', '卫衣', '毛衣', '风衣', '夹克', '裙子', '连衣裙', '短裤', '长裤'],
        "shoe": ['鞋', '靴', '拖鞋', '运动鞋', '皮鞋', '凉鞋', '袜子', '袜'],
        "hat": ['帽', '帽子', '围巾', '头巾', '发带', '鸭舌帽', '贝雷帽'],
        "glasses": ['眼镜', '墨镜', '太阳镜', '护目镜', '老花镜'],
        "bag": ['包', '背包', '手提包', '挎包', '钱包', '行李箱', '书包'],
        "accessory": ['饰品', '项链', '手链', '戒指', '耳环', '胸针', '腰带', '领带']
    }
    # 统一转为小写提升匹配容错（可选，视数据而定）
    title_lower = title.lower()
    # 遍历分类，检查是否包含任一关键词
    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword in title_lower:
                logger.debug(f"{title_lower}命中{category}")
                return category
    return None



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
        图1为某个人物的图像，包含其原始背景、姿态和表情；图2是帽子或围巾类商品的图像，商品可能出现在人物模特身上，但模特本身不应被包含在最终生成结果中。
        请将图2中的商品（仅限帽子或围巾）自然地“戴”或“围”到图1中的人物身上（帽子戴在头上，围巾围在颈部），确保商品的样式、颜色、纹理和图案完全保持不变，并仅使用商品本体部分，不包含图2中的任何人物主体或背景元素。
        具体要求如下：
        严格保留图1中人物的原始背景、姿态、表情和身材比例，仅添加或更换目标配饰；
        忽略图2中可能存在的人物模特形象，仅提取清晰的帽子或围巾区域作为素材使用；若图2背景杂乱或含有人体，应自动识别并去除，仅保留商品部分；
        商品需与人物身体部位自然贴合（如帽子贴合头型、围巾自然环绕颈部），比例协调，无违和感；
        细节丰富，材质与色彩真实还原，光影过渡自然，与原始图像的光线环境一致（如室内光、自然光）；
        避免出现商品漂浮、变形、位置错误或边缘不贴合等问题；禁止将图2中的人物以任何形式引入构图；
        图像清晰，可采用全身或半身视角，完整展示佩戴效果；
        整体风格贴近真实用户日常佩戴场景（如自拍、出门前照镜、冬季街拍等），光线自然，无商业影棚感，接近“买家秀”或生活记录照片效果；
        特别说明：图2中的商品若穿戴在模特身上，请智能抠除人物，仅保留配饰本身进行合成，确保最终图像中只出现图1人物与商品，不出现任何其他人物影像。
        """
    elif type=="shoe":
        prompt = f"""
        图1为某个人物的图像，包含其原始背景、姿态、表情和脚部状态；图2是鞋类或袜子类商品的图像。  
        请将图2中的商品自然地穿到人物的脚上（鞋子穿在脚上，袜子穿在脚上或鞋内），确保商品的样式、颜色、纹理和图案完全保持不变。  

        具体要求如下：  
        - 严格保留图1中人物的原始背景、姿态、表情和身材比例，仅更换或添加脚部穿戴商品；  
        - 商品需与脚部自然贴合，比例协调，无违和感（如鞋子包裹脚型、袜子平整无褶皱堆积）；  
        - 忽略商品图像的原始背景或者人物，仅提取商品主体进行融合；  
        - 细节丰富，材质与色彩真实还原，光影过渡自然，与原始图像的光线环境保持一致（如室内光、自然光、街拍光）；  
        - 避免出现商品漂浮、变形、位置错误或边缘不贴合等问题；  
        - 图像清晰高分辨率，建议采用全身或半身视角，完整展示脚部穿戴效果；  
        - 整体风格贴近真实用户日常穿着场景（如自拍、出门前、试鞋间、街头行走等），光线自然，无商业影棚打光感，接近“买家秀”或生活记录照片效果。
        """
    elif type=="glasses":
        prompt = f"""
        将图1中的普通用户作为人物基底，完整保留其原始姿态、表情、身材比例与透视角度；将图2中的目标商品（如眼镜、首饰等）从其背景中精准抠取，保持商品的样式、颜色、材质纹理、图案细节完全一致，不做任何修改。
        将该商品自然且贴合地穿戴或佩戴到人物相应身体部位（如面部、手部、颈部等），确保光影协调、透视一致、比例合理，无明显合成痕迹。
        移除商品原有的背景，仅保留商品主体进行无缝融合；人物的原始背景也无需保留，最终输出应为人物佩戴商品后的全身/半身像，背景简洁或透明，突出商品与人的融合效果。
        要求：真实感强，无违和感，商品不得变形、变色或被遮挡关键特征。 
        """
    else:
        prompt = f"""
        图1为一位普通用户的图像，包含其原始背景、姿态、表情和身材；图2是目标商品图像（可为鞋类、袜子、衣服、首饰、帽子、围巾等）。  
        请将该商品自然地穿到、戴到或配备到人物身上，确保商品的样式、颜色、纹理、图案完全保持不变。  
        商品原有背景或者人物无需保留，仅提取商品主体进行融合处理。  

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

