import os
import jenkinsapi
from template import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,DateTime,NVARCHAR,Integer,ForeignKey,UnicodeText,SMALLINT
from marathon import MarathonClient
from jenkinsapi.jenkins import Jenkins 
from flask import Module,render_template,Flask,request,url_for
from src.dcosconfig import *
jenkins = Module(__name__)

 
def get_server_instance():
    server = Jenkins(JENKINS)
#     server = Jenkins('http://127.0.0.1:8080')
    return server
@jenkins.route('/jenkins')
def get_job_details():
    # Refer Example #1 for definition of function 'get_server_instance'
#     server = get_server_instance()
#     for j in server.get_jobs():
#         job_instance = server.get_job(j[0])
#         print 'Job Name:%s' %(job_instance.name)
#         print 'Job Description:%s' %(job_instance.get_description())
#         print 'Is Job running:%s' %(job_instance.is_running())
#         print 'Is Job enabled:%s' %(job_instance.is_enabled())
    return render_template('CI/Create.html')   
@jenkins.route('/jenkins/job/stop/<taskcasename>',methods=['POST'])        
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
@jenkins.route('/jenkins/job/build/<taskcasename>')            
def job_build():
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()
    server.build_job('mesos',params=None)
def createjob():
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()
#     server.create_job('jobname', xml)
@jenkins.route('/jenkins/job/delete/<taskcasename>')
def deletejob():
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()
    server.delete_job('jobname2')

    
@jenkins.route('/jenkins/job/')    
def createjobconfig():
#     print request.data
#     print request.form()
    scmurl = 'svn://20.26.19.69/home/svn/svn_repository/Program/script/release'
    poll = 'H/5 * * * *'
    shell = 'sleep 5'
    typestatus = 0
    server = get_server_instance()
    config = jenkinsconfigfile
    config = config.replace('%SCMPATH%',scmurl)
    config = config.replace('%POLL%',poll )
    config = config.replace('%SHELL%', shell)
    server.create_job('jobname2', config)
    return 'ok'
@jenkins.route('/jenkins/job/update/<taskcasename>')
def updatejobconfig():
    scmurl = 'svn://20.26.19.69/home/svn/svn_repository/Program/script/release'
    poll = 'H/5 * * * *'
    shell = 'sleep 5 dir 1111 666 /home/test.sh\n'+"/home/test.sh"
    typestatus = 0
    server = get_server_instance()
    job = server.get_job("jobname2")
    config = jenkinsconfigfile
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

# with jenkins.test_request_context():
#     print  url_for('createjobconfig', next="dd")    
if __name__ == '__main__':

   print 'ok'