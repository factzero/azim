import uuid
from typing import Dict, List
from sqlalchemy import desc
import json

from db.models.images_store_model import ImgStoreModel
from db.session import with_session


@with_session
def add_image_to_db(session, name: str, path: str, modify_time, img_id=None):
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
    )
    session.add(m)
    session.commit()

    return m.id


@with_session
def del_image_from_db(session, img_id):
    del_img = session.query(ImgStoreModel).filter_by(img_id=img_id).first()
    if del_img:
        session.delete(del_img)
        session.commit()
    return True


@with_session
def paginated_image_from_db(session, page=1, per_page=10):
    order_by = desc(ImgStoreModel.modify_time)
    offset_v = (page - 1) * per_page
    events = session.query(ImgStoreModel).order_by(order_by).limit(per_page).offset(offset_v).all()
    events_list = [{"id": e.id, "name": e.name, "time": e.modify_time.isoformat(), "path": e.path} for e in events]
    return events_list


@with_session
def get_img_used_id(session, id):
    img = session.query(ImgStoreModel).filter_by(id=id).first()
    img_list = [{"id": img.id, "name": img.name, "time": img.modify_time.isoformat(), "path": img.path}] if img is not None else [None]   
    return img_list