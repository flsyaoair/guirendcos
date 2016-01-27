# -*- coding: UTF-8 -*- 
# import MySQLdb
from sqlalchemy import create_engine
from sqlalchemy.orm import Session,sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from math import  ceil
from src.dcosconfig import *

engine = create_engine(DB,echo=True)
BaseModel = declarative_base()

def get_session():
    
    return Session(bind = engine)

def drop_database():
    BaseModel.metadata.drop_all(bind=engine)

def create_database():
    BaseModel.metadata.create_all(bind=engine)
    
def query_more(alldata,order_by,page_no,page_size):
    row_count = alldata.count()
    page_count = int(ceil(row_count * 1.0 / page_size))
    if page_no < 1:
        page_no = 1
    if page_no > page_count:
        page_no = page_count
    if page_no == 0:
        page_no = 1
        page_count = 1
    data = alldata.order_by(order_by).limit(page_size * page_no).offset(0)
    return (data,row_count,page_count,page_no)