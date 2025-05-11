import os
import sys
sys.path.append(os.getcwd())

import requests


url = "http://127.0.0.1:9981/img/list/"

response = requests.get(url, params={"page": 1, "per_page": 1})
print(response.status_code)
if (response.status_code == 200):
    data = response.json()['images']
    print(data)
    for d in data:
        img_url = os.path.join("http://127.0.0.1:9981/img/get-img/", str(d['id']))
        res = requests.get(img_url)
        if (res.status_code == 200):
            buffer = res.content        
            with open(d['name'], "wb") as out_file:
                out_file.write(buffer)


# from db.base import create_tables
# from db.repository.images_store_repository import get_img_used_id

# create_tables()
# im = get_img_used_id(2)
# print(im)