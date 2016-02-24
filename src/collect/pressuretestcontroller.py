import os
import json
from flask import Module,Flask,request,jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import Session,sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,DateTime,NVARCHAR,Integer,ForeignKey,UnicodeText,SMALLINT,update
from marathon import MarathonClient
from time import sleep
from pip._vendor.distlib._backport.tarfile import TUREAD
from imageop import scale

pressuretest = Module(__name__)
@pressuretest.route('/')
def hello_jmeter():
    return 'Hello jmeter!'
@pressuretest.route('/jmeter/<jmeter>')
def jmeterconfig(jmeter):
    jmeterlist = jmeter.split('&')
    list = []
    for i in jmeterlist:
        p = i.split('=')
        p = p[1] 
        l = list.append(p)
    if  exist_category(list[0])==True:
        return "ok"
    else:
    
        (taskcasename,jmxname,threads,rampup,threadloop,SCALE) =tuple(list)  
        servicesCreate(taskcasename,jmxname,int(threads),int(rampup),int(threadloop),int(SCALE))
    
    
    return 'Hello jmeter!!!' 
@pressuretest.route('/jmeter/run/<id>')
def testcaserun(id):
#     c = MarathonClient(marathonip)
#     taskcasename = request.json['taskcasename']
    taskcasename = 'testcat'
    readed = json.load(open('temp.json', 'r'))
    readed['container']['docker']['image'] = dockerimage
    readed['id'] = taskcasename
    json.dump(readed, open('testcaseapp.json', 'w'))  
    os.system ('curl -X POST -H "Content-Type: application/json" %s/v2/apps -d@testcaseapp.json' %(marathonip))
#     task = c.list_tasks('myjenkins')
    taskcase = get(taskcasename)
    SCALE = taskcase.SCALE
    sleep(20)
    c.scale_app(taskcasename,instances=SCALE)

def testcasecreate():
    return 'ok'
@pressuretest.route('/jmeter/stop/<taskcasename>')
def testcasestop(taskcasename):
#     taskcasename = request.json['taskcasename']
    taskcasename = 'testcat'
    c.scale_app(taskcasename,instances=0)
    return True
@pressuretest.route('/jmeter/delete/<taskcasename>')    
def testcasedelete():
#     app_id = request.json['taskcasename']
    app_id = 'testcat'
    c.delete_app(app_id, force=True)
    return True
@pressuretest.route('/jmeter/update/<updatecontent>')
def testcaseupdate(updatecontent):
    updatecontentlist = updatecontent.split('&')
    list = []
    for i in updatecontentlist:
        p = i.split('=')
        p = p[1] 
        l = list.append(p)
    (taskcasename,jmxname,threads,rampup,threadloop,SCALE) =tuple(list) 
    task = update(id,taskcasename,jmxname,threads,rampup,threadloop,SCALE)
    return 'ok'


    
if __name__ == '__main__':

    print 'ok'
