from src.models.database import BaseModel
from sqlalchemy import Column,DateTime,NVARCHAR,Integer,ForeignKey,UnicodeText
class docker(BaseModel):

    __tablename__ = 'docker'
    DockerId = Column('DockerId', Integer,primary_key=True,nullable=False,autoincrement=True)
    TaskName = Column('TaskName', NVARCHAR(30),nullable = False)
    SCMUrl = Column('SCMUrl', NVARCHAR(30),nullable = False)
    Poll = Column('Poll', NVARCHAR(30),nullable = False)
    Shell = Column('Shell', NVARCHAR(30),nullable = False)
    TypeStatus = Column('TypeStatus', Integer,nullable=False)
    CREATEDATE = Column('CREATEDATE', DateTime,nullable=False)
class dockerServerModel(BaseModel):

    __tablename__ = 'dockerServerModel'
    ServiceModeld = Column('ServiceModeld', Integer,primary_key=True,nullable=False,autoincrement=True)
    NickName = Column('NickName', NVARCHAR(30),nullable = False)
    ImageType = Column('ImageType', NVARCHAR(30),nullable = False)
    ImageName = Column('ImageName', NVARCHAR(30),nullable = False)
    ContainerPort = Column('ContainerPort', Integer,nullable = False)
    HostPort = Column('HostPort', NVARCHAR(30),nullable=False)
    ContainerPath = Column('ContainerPath', NVARCHAR(30),nullable = False)
    HostPath = Column('HostPath', NVARCHAR(30),nullable = False)    
    CreateDate = Column('CreateDate', DateTime,nullable=False)
    LastUpdateDate = Column('LastUpdateDate', DateTime,nullable=False)
class dockerResourceModel(BaseModel):

    __tablename__ = 'dockerResourceModel'
    ResourceModelId = Column('ResourceModelId', Integer,primary_key=True,nullable=False,autoincrement=True)
    NickName = Column('NickName', NVARCHAR(30),nullable = False)
    Case = Column('Case', NVARCHAR(30),nullable=False)
    DockerCpu = Column('DockerCpu', NVARCHAR(30),nullable = False)
    DockerMemory = Column('DockerMemory', NVARCHAR(30),nullable = False)
    DockerVolume = Column('DockerVolume', NVARCHAR(30),nullable=False)
    CreateDate = Column('CreateDate', DateTime,nullable=False)
    LastUpdateDate = Column('LastUpdateDate', DateTime,nullable=False)    