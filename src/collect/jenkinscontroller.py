import os
import jenkinsapi
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,DateTime,NVARCHAR,Integer,ForeignKey,UnicodeText,SMALLINT
from marathon import MarathonClient
import template
from jenkinsapi.jenkins import Jenkins 
# from jenkinsapi.build import Build 
# from jenkinsapi import api
from flask import Flask,request,url_for
common = 0
release = 1
marathonip = 'http://20.26.17.133:8080'
# DB ='mysql+mysqlconnector://root:root@20.26.17.145:3306/dcos?charset=utf8'
DB ='mysql+mysqlconnector://root:root@127.0.0.1:3306/dcos?charset=utf8'

app = Flask(__name__)
engine = create_engine(DB,echo=True)
 
BaseModel = declarative_base()
c = MarathonClient(marathonip)

def create_database():
    BaseModel.metadata.create_all(bind=engine)
def drop_database():
    BaseModel.metadata.drop_all(bind=engine)
def get_session():
    
    return Session(bind = engine)
@app.route('/')
def hello_Jenkins():
    return 'Hello Jenkins!'

 
def get_server_instance():
    server = Jenkins('http://20.26.17.145:8089/jenkins')
#     server = Jenkins('http://127.0.0.1:8080')
    return server
# @app.route('/jenkins/job/<taskcasename>')
def get_job_details():
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()
    for j in server.get_jobs():
        job_instance = server.get_job(j[0])
        print 'Job Name:%s' %(job_instance.name)
        print 'Job Description:%s' %(job_instance.get_description())
        print 'Is Job running:%s' %(job_instance.is_running())
        print 'Is Job enabled:%s' %(job_instance.is_enabled())
@app.route('/jenkins/job/stop/<taskcasename>')        
def disable_job():
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()
    job_name = 'createImage'
    if (server.has_job(job_name)):
        job_instance = server.get_job(job_name)
        job_instance.disable()
        print 'Name:%s,Is Job Enabled ?:%s' %(job_name,job_instance.is_enabled()) 
def get_plugin_details():
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()
    for plugin in server.get_plugins().values():
        print dir(plugin)
        print "Short Name:%s" %(plugin.shortName)
        print "Long Name:%s" %(plugin.longName)
        print "Version:%s" %(plugin.version)
        print "URL:%s" %(plugin.url)
        print "Active:%s" %(plugin.active)
        print "Enabled:%s" %(plugin.enabled) 
@app.route('/jenkins/job/build/<taskcasename>')            
def job_build():
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()
    server.build_job('mesos',params=None)
def createjob():
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()
#     server.create_job('jobname', xml)
@app.route('/jenkins/job/delete/<taskcasename>')
def deletejob():
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()
    server.delete_job('jobname2')

    
@app.route('/jenkins/job/')    
def createjobconfig():
#     print request.data
#     print request.form()
    scmurl = 'svn://20.26.19.69/home/svn/svn_repository/Program/script/release'
    poll = 'H/5 * * * *'
    shell = 'sleep 5'
    typestatus = 0
    server = get_server_instance()
    config = template.jenkinsconfigfile
    config = config.replace('%SCMPATH%',scmurl)
    config = config.replace('%POLL%',poll )
    config = config.replace('%SHELL%', shell)
    server.create_job('jobname2', config)
    return 'ok'
@app.route('/jenkins/job/update/<taskcasename>')
def updatejobconfig():
    scmurl = 'svn://20.26.19.69/home/svn/svn_repository/Program/script/release'
    poll = 'H/5 * * * *'
    shell = 'sleep 5 dir 1111 666 /home/test.sh\n'+"/home/test.sh"
    typestatus = 0
    server = get_server_instance()
    job = server.get_job("jobname2")
    config = template.jenkinsconfigfile
    config = config.replace('%SCMPATH%',scmurl)
    config = config.replace('%POLL%',poll )
    config = config.split('\n')
    list = []
    sl = ''
    for i in config:
        list.append(i.strip())
    config = sl.join(list)
    config = config.replace('%SHELL%', shell)  
    job.update_config(config)
    print 'ok'   
class JenkinsTask(BaseModel):

    __tablename__ = 'JenkinsTask'
    JenkinsTaskId = Column('JenkinsTaskId', Integer,primary_key=True,nullable=False,autoincrement=True)
    TaskName = Column('TaskName', NVARCHAR(30),nullable = False)
    SCMUrl = Column('SCMUrl', NVARCHAR(30),nullable = False)
    Poll = Column('Poll', NVARCHAR(30),nullable = False)
    Shell = Column('Shell', NVARCHAR(30),nullable = False)
    TypeStatus = Column('TypeStatus', Integer,nullable=False)

def servicesCreate(taskname,scmurl,poll,shell,typestatus):
#     database = get_session()
    session = get_session()
    T = JenkinsTask()
    T.TaskName = taskname
    T.SCMUrl = scmurl
    T.Poll = poll
    T.Shell = shell
    T.TypeStatus = typestatus
    session.add(T)
    session.commit()
    session.close()
def delete(id):
    session = get_session()
    session.query(JenkinsTask).filter(JenkinsTask.JenkinsTaskId == id).delete()
    session.commit()
    session.close()    
def update(id,taskname,scmurl,poll,shell):
#     taskcasename ='cc'
    session = get_session()

    task = session.query(JenkinsTask).filter(JenkinsTask.JenkinsTaskId == id).update({'TaskName':taskname,'SCMUrl':scmurl,'Poll':poll,'Shell':shell})

    session.commit()
    session.close()
with app.test_request_context():
    print  url_for('createjobconfig', next="dd")    
if __name__ == '__main__':
#     print get_server_instance().version 
#     get_job_details() 
#     disable_job()
#     get_plugin_details()
#     job_build()
#     createjob()  
#     createjobconfig()
    create_database()

#     updatejobconfig()
#     app.run(host= '10.73.144.234',port=5002)
#     app.run(host= '10.70.86.39',port=5002)
    app.run(host= '127.0.0.1',port=5002)