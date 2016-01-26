# -*- coding: UTF-8 -*- 
from src.models.database import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column,DateTime,NVARCHAR,Integer,ForeignKey,UnicodeText
class projectProfile(BaseModel):

    __tablename__ = 'projectProfile'
    Id = Column('Id', Integer,primary_key=True,nullable=False,autoincrement=True)
    ProjectKey = Column('ProjectKey', NVARCHAR(30),nullable = False)
    DockerProfile = Column('DockerProfile', NVARCHAR(200),nullable = False)
    CreateDate = Column('CreateDate', DateTime,nullable=False)
    LastUpdateDate = Column('LastUpdateDate', DateTime,nullable=False)