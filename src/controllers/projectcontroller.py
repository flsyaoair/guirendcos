# -*- coding: UTF-8 -*- 
import json
import os
from flask import Module,render_template,jsonify,request,g
from src.dcosconfig import *
from src.services import dockerservice,projectservice
project = Module(__name__)
@project.route('/App/Create',methods=['POST'])
#config docker profile
def createApp ():
        projectname = request.json['ProjectName']
        projectkey = request.json['ProjectKey']
        packagegettype = request.json['PackageGetType']
        servermodel_id = request.json['ServerModelId']
        resourcemodel_id = request.json['ResourceModelId']
        scmurl = request.json['SCMUrl']
        poll = request.json['Poll']
        shell = request.json['Shell']
        status = request.json['Status']
        sl = dockerservice.serverModelList(servermodel_id)
        rl = dockerservice.resourceModelList(resourcemodel_id)
        resourcemodeldict = {"Case":rl.Case,"DockerCpu":rl.DockerCpu,"DockerMemory":rl.DockerMemory,"DockerVolume":rl.DockerVolume}
        servermodeldict = {"ImageName":sl.ImageName,"ContainerPort":sl.ContainerPort,"HostPort":sl.HostPort,"ContainerPath":sl.ContainerPath,"HostPath":sl.HostPath
        }
        
        try:
           readed = json.load(open('src/static/model/docker/temp.json', 'r'))
        except Exception,e:
           print Exception,':',e
        readed['container']['docker']['image'] = sl.ImageName
        name = readed['id'] 
        json.dump(readed, open('src/static/model/docker/app.json', 'w'))
        dockerprofile=dict(resourcemodeldict, **servermodeldict)
        dockerprofile = str(dockerprofile)

#         eval(a)
        projectservice.create_project(projectname,projectkey,packagegettype,scmurl,poll,shell,status)
        projectservice.create_projectProfile(projectkey,dockerprofile)
        

#         pathList = request.json['PathList']
#     try:
#         containerpath = request.json['ContainerPath']
#         hostpath = request.json['HostPath']
#     except KeyError,e:
#         containerpath = ''
#         hostpath = ''
#     if (request.json['ProjectName'] != '') & (request.json['ProjectKey'] != ''):
#         exist = dockerservice.create(request.json['ProjectName'],request.json['ProjectKey'],Introduction,g.user_id)
#         empty = False
#     else :
#         exist = True
#         empty = True
#     exist_json = {'exist': exist, 'empty': empty}
#         return jsonify("Ture")
        return jsonify(created=True)
    
    
@project.route('/Container/ServerModel/Update',methods=['POST'])
def serverModelUpdate():
        servermodel_id = request.json['ServerModelId']
        imagename = request.json['ImageName']
        containerport = request.json['ContainerPort']    
        hostport = request.json['HostPort']
        containerpath = request.json['ContainerPath']
        hostpath = request.json['HostPath']
        dockerservice.update_dockerservermodel(servermodel_id,imagename,containerport,hostport,containerpath,hostpath)
        return jsonify(updated=True)

@project.route('/Container/ServerModel/Delete',methods=['POST'])
def serverModelDelete():
    dockerservice.serverModelDelete(request.json['ServerModelId'])
    return jsonify(deleted=True)    



if __name__ == '__main__':
    dockerservice.resourceModelList(1)
    dockerservice.serverModelList(1)   
    