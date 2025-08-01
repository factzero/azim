import os
import uuid
from typing import Dict, List
from sqlalchemy import desc

from db.models.images_store_model import ImgStoreModel
from db.session import with_session


# 自定义域名或 IP（可通过环境变量注入）
base_url = os.getenv("BASE_URL", "http://localhost:9981/img/get-img")

@with_session
def add_image_to_db(session, name: str, path: str, modify_time, img_id=None, feature=None):
    """
    新增图片
    """
    if not img_id:
        img_id = uuid.uuid4().hex
    m = ImgStoreModel(
        img_id=img_id,
        name=name,
        path=path,
        modify_time=modify_time,
        feature=feature,
    )
    session.add(m)
    session.commit()

    return 'success', f"{base_url}/{img_id}"


@with_session
def del_image_from_db(session, img_id):
    del_img = session.query(ImgStoreModel).filter_by(img_id=img_id).first()
    if del_img:
        session.delete(del_img)
        session.commit()
    return True


@with_session
def update_image_feature(session, img_id: str, feature: dict):
    """
    根据 img_id 更新图片特征
    """
    img = session.query(ImgStoreModel).filter_by(img_id=img_id).first()
    if not img:
        return False

    img.feature = feature
    session.commit()
    return True


@with_session
def get_image_feature(session, img_id: str):
    """
    根据 img_id 获取图片特征
    """
    img = session.query(ImgStoreModel).filter_by(img_id=img_id).first()
    if not img:
        return None
    return img.feature


@with_session
def paginated_image_from_db(session, page=1, per_page=10):
    order_by = desc(ImgStoreModel.modify_time)
    offset_v = (page - 1) * per_page
    events = session.query(ImgStoreModel).order_by(order_by).limit(per_page).offset(offset_v).all()
    events_list = [{"id": e.id, "name": e.name, "time": e.modify_time.isoformat(), "path": e.path} for e in events]
    return events_list


@with_session
def get_all_images_info(session) -> List[Dict]:
    """
    获取所有图片数据
    """
    order_by = desc(ImgStoreModel.modify_time)
    images = session.query(ImgStoreModel).order_by(order_by).all()
     
    return [
        {
            "id": image.id,
            "img_id": image.img_id,
            "name": image.name,
            "time": image.modify_time.strftime("%Y-%m-%d"),
            "url": f"{base_url}/{image.img_id}"
        }
        for image in images
    ]


@with_session
def get_img_used_img_id(session, img_id):
    img = session.query(ImgStoreModel).filter_by(img_id=img_id).first()
    img_list = [{"id": img.id, "name": img.name, "time": img.modify_time.isoformat(), "path": img.path}] if img is not None else [None]   
    return img_list