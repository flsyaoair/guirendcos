from src.models.database import BaseModel
from sqlalchemy import Column,DateTime,NVARCHAR,Integer,ForeignKey,UnicodeText

class dockerServerModel(BaseModel):

    __tablename__ = 'dockerServerModel'
    ServerModelId = Column('ServerModelId', Integer,primary_key=True,nullable=False,autoincrement=True)
    NickName = Column('NickName', NVARCHAR(60),nullable = False)
    ImageType = Column('ImageType', NVARCHAR(30),nullable = False)
    ImageName = Column('ImageName', NVARCHAR(100),nullable = False)
    ContainerPort = Column('ContainerPort', Integer,nullable = False)
    HostPort = Column('HostPort', NVARCHAR(30),nullable=False)
    ContainerPath = Column('ContainerPath', NVARCHAR(30),nullable = False)
    HostPath = Column('HostPath', NVARCHAR(30),nullable = False)    
    CreateDate = Column('CreateDate', DateTime,nullable=False)
    LastUpdateDate = Column('LastUpdateDate', DateTime,nullable=False)
class dockerResourceModel(BaseModel):

    __tablename__ = 'dockerResourceModel'
    ResourceModelId = Column('ResourceModelId', Integer,primary_key=True,nullable=False,autoincrement=True)
    NickName = Column('NickName', NVARCHAR(60),nullable = False)
    Case = Column('Case', NVARCHAR(30),nullable=False)
    DockerCpu = Column('DockerCpu', NVARCHAR(30),nullable = False)
    DockerMemory = Column('DockerMemory', NVARCHAR(30),nullable = False)
    DockerVolume = Column('DockerVolume', NVARCHAR(30),nullable=False)
    CreateDate = Column('CreateDate', DateTime,nullable=False)
    LastUpdateDate = Column('LastUpdateDate', DateTime,nullable=False)    