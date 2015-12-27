import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session,sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,DateTime,NVARCHAR,Integer,ForeignKey,UnicodeText,SMALLINT
DB ='mysql+mysqlconnector://root:root@20.26.17.145:3306/performancetest?charset=utf8' 
HOST = '10.73.144.234:5001/jmeter/remoteclient'
# HOST = '10.73.144.234:5001/jmeter/remoteclient'
# DB = 'oracle+cx_oracle://icloud:icloud@20.26.2.26:1521/cloud'
engine = create_engine(DB,echo=True)
BaseModel = declarative_base()
def get_session():
    
    return Session(bind = engine)
class TestTask(BaseModel):

    __tablename__ = 'TestTask'
    TestTaskId = Column('TestTaskId', Integer,primary_key=True,nullable=False,autoincrement=True)
    TaskCaseName = Column('TaskCaseName', NVARCHAR(30),nullable = False)
    JmxName = Column('JmxName', NVARCHAR(30),nullable = False)
    Threads = Column('Threads', Integer,nullable=False)
    RampUp = Column('RampUp', Integer,nullable=False)
    ThreadLoop = Column('ThreadLoop', Integer,nullable=False)
    SCALE = Column('SCALE', Integer,nullable=False)
def get(taskcasename):
    session = get_session()
    taskcase = session.query(TestTask).filter(TestTask.TaskCaseName == taskcasename).one()
    return taskcase   
def getconfig():

    appname ='testcase'
    data = """'{"taskcasename":"%appid%"}'"""
    data = data.replace('%appid%',appname)
    cc =os.system( "curl -i -X POST -H 'Content-Type: application/json' -d %s %s > config"  %(data, HOST))
    config = open('config','r')
    
    l = []
    sl = ''
    for i in config :
        l.append(i)
    c= ''.join(l)
    c= c[c.find('{'):c.find('}')+1]
    c =eval(c)
    JmxName = c["JmxName"]
    return c
def update():
#     appid = os.getenv("MARATHON_APP_ID")
    appid = "testcat"
    appname ='testcat'
    data = """'{"taskcasename":"%appid%"}'"""
    data = data.replace('%appid%',appname)
    print data
    cc =os.system( "curl -i -X POST -H 'Content-Type: application/json' -d %s %s > config"  %(data, HOST))
    config = open('config','r')
    
    l = []
    sl = ''
    for i in config :
        l.append(i)
    c= ''.join(l)
    print c
    c= c[c.find('{'):c.find('}')+1]
    c =eval(c)

    taskcase = c
    jmxname = taskcase['JmxName']
    rampup = taskcase['RampUp']
    rampup = str(rampup)
    threadloop = taskcase['ThreadLoop']
    threadloop = str(threadloop)
    SCALE = taskcase['SCALE']
    threads = taskcase['Threads'] 
    threads = str(threads)
    buildxml = open('buildtemp.xml','r').readlines()
    xml = open('build.xml','w')
    for l in buildxml:
        xml.write(l.replace('%appid%',appid).replace('%jmx%',jmxname).replace('%rampUp%',rampup).replace('%threads%',threads).replace('%threadloop%',threadloop))
    xml.close()

if __name__ == '__main__':
     update()
      