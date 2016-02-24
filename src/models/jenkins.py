from src.models.database import BaseModel
from sqlalchemy import Column,DateTime,NVARCHAR,Integer,ForeignKey,UnicodeText
class JenkinsTask(BaseModel):

    __tablename__ = 'JenkinsTask'
    JenkinsTaskId = Column('JenkinsTaskId', Integer,primary_key=True,nullable=False,autoincrement=True)
    TaskName = Column('TaskName', NVARCHAR(30),nullable = False)
    SCMUrl = Column('SCMUrl', NVARCHAR(30),nullable = False)
    Poll = Column('Poll', NVARCHAR(30),nullable = False)
    Shell = Column('Shell', NVARCHAR(30),nullable = False)
    TypeStatus = Column('TypeStatus', Integer,nullable=False)