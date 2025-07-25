from sqlalchemy import JSON, Column, DateTime, Integer, String, func

from db.base import Base


class ImgStoreModel(Base):
    """
    图片存储
    """

    __tablename__ = "imgs"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")
    img_id = Column(String(32), comment="images ID")
    name = Column(String(256), comment="文件名")
    path = Column(String(1024), comment="图片存储路径")
    modify_time = Column(DateTime, default=func.now(), comment="图片修改时间")
    create_time = Column(DateTime, default=func.now(), comment="图片保存至数据库的时间")
    
    feature = Column(JSON, comment="图片特征向量")

    def __repr__(self):
        return f"<message(id='{self.id}', name='{self.name}', modify_time='{self.modify_time}')>"
