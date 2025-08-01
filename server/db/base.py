from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker


# engine = create_engine('sqlite:///store/azim-img.db', echo=True)
engine = create_engine('sqlite:///store/azim-img.db')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base: DeclarativeMeta = declarative_base()


def create_tables():
    Base.metadata.create_all(bind=engine)
