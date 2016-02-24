# -*- coding: UTF-8 -*- 

from src.models.database import BaseModel

from sqlalchemy import Column, Boolean,DateTime,NVARCHAR,SMALLINT,VARCHAR,Integer

class UserStatus:
    Enabled = 1
    Disabled = 2

class UserProfile(BaseModel):

    __tablename__ = 'UserProfile'
    UserId = Column('UserId', Integer,primary_key=True,nullable=False,autoincrement=True)
    Email = Column('Email', VARCHAR(255),nullable=False,unique=True)
    Nick = Column('Nick', NVARCHAR(10),nullable = False)
    Password = Column('Password', VARCHAR(20),nullable=False)
    Status = Column('Status', SMALLINT,nullable = False)
    IsAdmin = Column('IsAdmin', Boolean,nullable=False)
    RegDate = Column('RegDate', DateTime,nullable=False)