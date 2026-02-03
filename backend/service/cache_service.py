import json
import os


def get_cache_data(key):
    if not os.path.exists(f'./cache/{key}.json'):
        return None
    with open(f'./cache/{key}.json', 'r',encoding="utf-8") as f:
        return json.load(f)

def set_cache_data(key, value):
    with open(f'./cache/{key}.json', 'w',encoding="utf-8") as f:
        json.dump(value,f,indent=4,ensure_ascii=False)
    return True

