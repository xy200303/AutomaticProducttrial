import asyncio

from backend.service.image_service import dashscope_try_on, encode_file
from backend.utils import parse_short_url


async def t():
    # print(await parse_short_url("https://e.tb.cn/h.7sPuh7QAcW2G55T?tk=mydSU8MeX25"))
    res=await dashscope_try_on(
        type="111",
        good_img=encode_file("./good1.png"),
        person_img=encode_file("./person.png"),
    )
    print(res)
if __name__ == "__main__":
    asyncio.run(t())