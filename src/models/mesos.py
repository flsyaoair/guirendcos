# -*- coding: UTF-8 -*- 
from src.models.database import BaseModel
# from testTeam.models.userprofile import UserProfile
# from testTeam.models.project import Project
from sqlalchemy import Column,DateTime,NVARCHAR,Integer,ForeignKey,UnicodeText

class mesos(BaseModel):   
    __tablename__ = 'mesos'
    CluId = Column('Id', Integer,primary_key=True,nullable=False,autoincrement=True)
#     App = Column('app_name', Integer,nullable = False) 
    CpusTotal = Column('CpusTotal', NVARCHAR(30),nullable=False)
    MemTotal = Column('MemTotal', NVARCHAR(30),nullable=False)
    DiskTotal = Column('DiskTotal', NVARCHAR(30),nullable=False)
    DiskUsed = Column('DiskUsed', NVARCHAR(30),nullable=False)
    CpusUsed = Column('CpusUsed', NVARCHAR(30),nullable=False)
    MemUsed = Column('MemUsed', NVARCHAR(30),nullable=False)       
#     ProjectId = Column('ProjectId', Integer,ForeignKey('Project.ProjectId'),nullable = False) 
#     Creator = Column('Creator', Integer,ForeignKey('UserProfile.UserId'),nullable = False)
#     Description = Column('Description', UnicodeText)
    CreateDate = Column('CreateDate', DateTime,nullable=False)
#     LastUpdateDate = Column('LastUpdateDate', DateTime,nullable=False)    
#     DownCount = Column('DownCount', Integer, nullable=True)