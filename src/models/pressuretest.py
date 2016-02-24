from src.models.database import BaseModel
from sqlalchemy import Column,DateTime,NVARCHAR,Integer,ForeignKey,UnicodeText
class TEST_TASK(BaseModel):

    __tablename__ = 'TEST_TASK'
    TestTaskId = Column('TestTaskId', Integer,primary_key=True,nullable=False,autoincrement=True)
    TaskCaseName = Column('TaskCaseName', NVARCHAR(30),nullable = False)
    JmxName = Column('JmxName', NVARCHAR(30),nullable = False)
    Threads = Column('Threads', Integer,nullable=False)
    RampUp = Column('RampUp', Integer,nullable=False)
    ThreadLoop = Column('ThreadLoop', Integer,nullable=False)
    SCALE = Column('SCALE', Integer,nullable=False)
