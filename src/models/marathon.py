# -*- coding: UTF-8 -*- 
from src.models.database import BaseModel
# from testTeam.models.userprofile import UserProfile
# from testTeam.models.project import Project
from sqlalchemy import Column,DateTime,NVARCHAR,Integer,ForeignKey,UnicodeText

class marathon(BaseModel):   
    __tablename__ = 'marathon'
    AppId = Column('AppId', Integer,primary_key=True,nullable=False,autoincrement=True)
    AppName = Column('AppName', NVARCHAR(30),nullable=False)
    Cpus = Column('Cpus', NVARCHAR(30),nullable=False)
    Mem = Column('Mem', NVARCHAR(30),nullable=False)
    Disk = Column('Disk', NVARCHAR(30),nullable=False)
    DockerImage = Column('DockerImage', NVARCHAR(30),nullable=False)
    Port = Column('Port', NVARCHAR(30),nullable=False)
    Host = Column('Host', NVARCHAR(30),nullable=False)       
#     ProjectId = Column('ProjectId', Integer,ForeignKey('Project.ProjectId'),nullable = False) 
#     Creator = Column('Creator', Integer,ForeignKey('UserProfile.UserId'),nullable = False)
#     Description = Column('Description', UnicodeText)
    CreateDate = Column('CreateDate', DateTime,nullable=False)
#     LastUpdateDate = Column('LastUpdateDate', DateTime,nullable=False)    
#     DownCount = Column('DownCount', Integer, nullable=True)