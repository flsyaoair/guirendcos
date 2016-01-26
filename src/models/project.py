# -*- coding: UTF-8 -*- 
from src.models.database import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column,DateTime,NVARCHAR,Integer,ForeignKey,UnicodeText
class project(BaseModel):

    __tablename__ = 'project'
    ProjectId = Column('ProjectId', Integer,primary_key=True,nullable=False,autoincrement=True)
    ProjectName = Column('ProjectName', NVARCHAR(60),nullable = False)
    ProjectKey = Column('ProjectKey', NVARCHAR(60),nullable = False)
    PackageGetType = Column('PackageGetType', NVARCHAR(30),nullable = False)
    SCMUrl = Column('SCMUrl', NVARCHAR(500),nullable = False)
    Poll = Column('Poll', NVARCHAR(30),nullable = False)
    Shell = Column('Shell', NVARCHAR(500),nullable = False)
    Status = Column('Status', Integer,nullable=False)
    CreateDate = Column('CreateDate', DateTime,nullable=False)
    LastUpdateDate = Column('LastUpdateDate', DateTime,nullable=False)