from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db.db_conf import sqlite

engine = create_engine(sqlite.DATABASE_URL_sqlite)
Base = declarative_base()

class Posts(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    img_id = Column(String)
    img = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()