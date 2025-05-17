import os
import sys
sys.path.append(os.getcwd())

import requests


response = requests.get("http://127.0.0.1:9981/img/get-all-imgs-info")
print(response.status_code)
if (response.status_code == 200):
    data = response.json()['images']
    print(data)
    for d in data:
        print(d['url'])
        res = requests.get(d['url'])
        if (res.status_code == 200):
            print("OK")


# from db.base import create_tables
# from db.repository.images_store_repository import get_img_used_id

# create_tables()
# im = get_img_used_id(2)
# print(im)