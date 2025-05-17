import os
from fastapi import APIRouter, File, UploadFile, Form, Query
from fastapi.responses import JSONResponse, FileResponse
import uuid
import shutil

from db.repository.images_store_repository import add_image_to_db, paginated_image_from_db, get_img_used_img_id, get_all_images_info
from utils import get_file_modify_time


imgs_router = APIRouter(prefix="/img", tags=["Image Operation"])

# 设置图片存储目录
UPLOAD_DIR = "./uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

STORE_IMG_DIR = './store'
if not os.path.exists(STORE_IMG_DIR):
    os.makedirs(STORE_IMG_DIR)


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

        img_id = add_image_to_db(name=file.filename, path=dest_file, modify_time=file_time, img_id=img_id)
        
        return {"filename": file.filename, "path": dest_file}
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