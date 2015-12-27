from flask import Module,render_template,jsonify, redirect, request, session, g
import time
from marathon import MarathonClient
from marathon.models.base import MarathonResource
from marathon.models.app import MarathonTaskFailure
import cmconfig
from src.models.marathon import marathon
from src.services import marathonservice
# from configmanage.cmconfig import *
# print type(MARATHON)
marathon = Module(__name__)
# case.before_request(login_filter)
# print MARATHON
c = MarathonClient(cmconfig.MARATHON)
def marathoncollet():    
    appmetrics = c.get_metrics()
    appsIdList = c.list_apps()
    ist_length = len(appsIdList)
    applist = {}
    tasklist = {}
    for i in range(ist_length):
#         print i
#         print appsIdList[i]
        appID = appsIdList[i].id
        cpus = appsIdList[i].cpus
        disk = appsIdList[i].disk
        mem = appsIdList[i].mem
        ports  = appsIdList[i].ports
        # last_task_failure = appsIdList[i].last_task_failure 
        # uris  = appsIdList[i].uris 
        tasks_staged  = appsIdList[i].tasks_staged 
     
        ###########container####################
        port_mappings = appsIdList[i].container.docker.port_mappings
        # Dtype = appsIdList[i].container.docker.type
        dockerimages = appsIdList[i].container.docker.image
        volumes  = appsIdList[i].container.volumes 
        
        task = c.list_tasks(appID)
        t = MarathonTaskFailure()
        for i in task:       
            t = MarathonTaskFailure()
            
#             return appID,i.host,i.ports,i.staged_at,i.started_at
            print appID,cpus,disk,mem,ports,dockerimages,i.host,i.ports,i.staged_at,i.started_at
            marathonservice.create_marathon(appID,cpus,disk,mem,ports,dockerimages,i.host,i.ports)
         
        
        # print port_mappings
# marathoncollet()        
#         cmFile=open('cm.txt','w')
    #     cmFile.write(images)
#         cmFile.close()
# def create():
#     print "rrrrrrrrrrrrrrrrrrrrrrrrrrr"
#     c=marathoncollet()
#     print c
#     appID = c.appID
#     disk = c.disk
#     cpus = c.cpus
#     mem = c.mem
#     dockerimages = c.dockerimages
#     ports = c.ports 
#     print ports
           
# print containerPort

# for i in appsIdList:
#  
#     print i
#     appid=i.rsplit('::/')[i]
#     print appid
#     taskList = c.list_tasks(appid)

# app=c.
# print leader,marathon_config
# print taskList
# print app2['"reconciliationInterval"']
# def create():
    
# create()