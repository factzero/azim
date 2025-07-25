import os
import yaml
from fastapi import APIRouter, File, UploadFile, Form, Query
from fastapi.responses import JSONResponse, FileResponse
import uuid
import shutil
import requests

from db.repository.images_store_repository import add_image_to_db, paginated_image_from_db, get_img_used_img_id, get_all_images_info, update_image_feature, get_image_feature
from utils import get_file_modify_time


imgs_router = APIRouter(prefix="/img", tags=["Image Operation"])

with open("server.yaml", "r") as f:
    config = yaml.safe_load(f)
    
AI_CONFIG = config["AI"]
AI_SERVER_PATH = str(AI_CONFIG["server"]["ip"]) + ":" + str(AI_CONFIG["server"]["port"])

# 设置图片存储目录
UPLOAD_DIR = "./uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

STORE_IMG_DIR = './store'
if not os.path.exists(STORE_IMG_DIR):
    os.makedirs(STORE_IMG_DIR)


import json

# import httpx
@imgs_router.post("/upload")
async def upload_image(file: UploadFile = File(...), mod_time: str = Form(...)):
    try:
        # 确保文件是图片类型
        if not file.content_type.startswith('image/'):
            return JSONResponse(status_code=400, content={"message": "Only image files are allowed."})

        # 保存上传的文件到指定目录
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())

        # 获取文件修改时间
        mod_time_float = float(mod_time)
        os.utime(file_location, (mod_time_float, mod_time_float))
        
        file_time = get_file_modify_time(file_location)
        new_folder_name = file_time.strftime('%Y-%m')
        new_folder_path = os.path.join(STORE_IMG_DIR, new_folder_name)
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)

        img_id = uuid.uuid4().hex
        dest_file = os.path.join(new_folder_path, img_id+'-'+file.filename)
        shutil.move(file_location, dest_file)

        imgStatus, url = add_image_to_db(name=file.filename, path=dest_file, modify_time=file_time, img_id=img_id)
        
        try:
            print("AI_SERVER_PATH: ", AI_SERVER_PATH)
            print("url: ", url)
            image_path = os.path.join(os.getcwd(), dest_file)
            print("image_path: ", image_path)
            img_response = requests.post(AI_SERVER_PATH + "/ai/img_feature", json={"path": image_path}, timeout=20)
            img_feature = img_response.json()["feature"]
            update_image_feature(img_id, {"img" : img_feature})
        except Exception as e:
            print(e)
        
        return {'status': imgStatus, "filename": file.filename, "url": url}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@imgs_router.get("/list")
async def list_images(
    page: int = Query(1, ge=1),  # 第几页，默认第一页
    per_page: int = Query(10, ge=1, le=100)  # 每页多少项，默认10项，最大100项
):
    images_info = paginated_image_from_db(page, per_page)
    
    return {"images": images_info}


@imgs_router.get("/get-all-imgs-info")
async def get_all_imgs_info():
    imgs_info = get_all_images_info()
    return {"images": imgs_info}


@imgs_router.get("/get-img/{img_id}")
async def get_img(img_id: str):
    im = get_img_used_img_id(img_id)
    if len(im) == 0:
        return JSONResponse(status_code=500, content={"message": "Image ID not found"})
    if not os.path.exists(im[0]['path']):
        return JSONResponse(status_code=500, content={"message": "Image PATH not found"})
    
    return FileResponse(im[0]['path'], media_type='image/jpeg')


from typing import Optional
from pydantic import BaseModel


class SearchInput(BaseModel):
    txt: Optional[str] = None
    

import numpy as np

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    
    # 归一化
    a_norm = a / np.linalg.norm(a)
    b_norm = b / np.linalg.norm(b)
    
    # 点积
    return np.dot(a_norm, b_norm)

@imgs_router.post("/search")
async def search_imgs(input: SearchInput):
    if input.txt is None:
        return JSONResponse(status_code=400, content={"message": "Please input text"})
    
    thre = AI_CONFIG["search"]["thre"]
    
    try:
        print("AI_SERVER_PATH: ", AI_SERVER_PATH)
        response = requests.post(AI_SERVER_PATH + "/ai/txt_feature", json={"txt": input.txt}, timeout=20)
        if response.status_code != 200:
            return JSONResponse(status_code=500, content={"message": "AI server error"})
        
        txt_feature = response.json()["feature"]
        imgs_info = get_all_images_info()
        matched_imgs = []
        for img_info in imgs_info:
            img_feature = get_image_feature(img_info["img_id"])
            sim = cosine_similarity(img_feature["img"][0], txt_feature[0])
            print("sim: ", sim)
            if sim > thre :
                matched_imgs.append({"img_info": img_info, "similarity": sim})
            
        # 按相似度从高到低排序
        matched_imgs.sort(key=lambda x: x["similarity"], reverse=True)
                
        return {"images": [item["img_info"] for item in matched_imgs]}
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"message": str(e)})    
