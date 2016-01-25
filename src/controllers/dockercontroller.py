# -*- coding: UTF-8 -*- 
import json
import os
from flask import Module,render_template,jsonify,request,g
from src.dcosconfig import *
from src.services import dockerservice
docker = Module(__name__)
@docker.route('/Container/ServerModel',methods=['POST'])
#config docker profile
def createContainerServerModel ():
        nickname = request.json['NickName']
        imagetype = request.json['ImageType']
        imagename = request.json['ImageName']
        containerport = request.json['ContainerPort']    
        hostport = request.json['HostPort']
        containerpath = request.json['ContainerPath']
        hostpath = request.json['HostPath']
       
        dockerservice.create_dockerservermodel(nickname,imagetype,imagename,containerport,hostport,containerpath,hostpath)

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
    
    
@docker.route('/Container/ServerModel/Update',methods=['POST'])
def serverModelUpdate():
        servermodel_id = request.json['ServerModelId']
        imagename = request.json['ImageName']
        containerport = request.json['ContainerPort']    
        hostport = request.json['HostPort']
        containerpath = request.json['ContainerPath']
        hostpath = request.json['HostPath']
        dockerservice.update_dockerservermodel(servermodel_id,imagename,containerport,hostport,containerpath,hostpath)
        return jsonify(updated=True)

@docker.route('/Container/ServerModel/Delete',methods=['POST'])
def serverModelDelete():
    dockerservice.serverModelDelete(request.json['ServerModelId'])
    return jsonify(deleted=True)    

@docker.route('/Container/ResourceModel',methods=['POST'])
def createContainerResourceModel ():
        nickname = request.json['NickName']
        case = request.json['Case']
        dockercpu = request.json['DockerCpu']
        dockermemory = request.json['DockerMemory']
        dockervolume = request.json['DockerVolume'] 
        dockerservice.create_dockerresourcemodel(nickname,case,dockercpu,dockermemory,dockervolume) 
        return jsonify(created=True)
    

@docker.route('/Container/ResourceModel/Update',methods=['POST'])
def resourceModelUpdate():
        resourcemodel_id = request.json['ResourceModelId']
        case = request.json['Case']
        dockercpu = request.json['DockerCpu']
        dockermemory = request.json['DockerMemory']
        dockervolume = request.json['DockerVolume'] 
        dockerservice.update_dockerresourcemodel(resourcemodel_id, case, dockercpu, dockermemory, dockervolume)
        return jsonify(updated=True)

@docker.route('/Container/ResourceModel/Delete',methods=['POST'])
def resourceDelete():
    dockerservice.resourceModelDelete(request.json['ResourceModelId'])
    return jsonify(deleted=True)    
def resourceModelList():
    resouceModel_list = dockerservice.query_resourceModelList()
    return render_template('ResourceModel/List.html',resouceModellist=resouceModel_list) 
def serverModelList():
    serverModel_list = dockerservice.query_serverModelList()
    return render_template('ServerModel/List.html',serverModellist=serverModel_list)   


@docker.route('/Container/MergeModel',methods=['POST'])     
def MergeContainerProfile(servermodelid,resourcemodelid):
        try:
           readed = json.load(open('src/static/model/docker/temp.json', 'r'))
        except Exception,e:
           print Exception,':',e
        readed['container']['docker']['image'] = createContainerServerModel.imagename
        name = readed['id'] 
        json.dump(readed, open('src/static/model/docker/app.json', 'w'))
        return 'ok'    
@docker.route('/Container/commit',methods=['POST'])     
def createContainerProfile():
        
        try:
           readed = json.load(open('src/static/model/docker/temp.json', 'r'))
        except Exception,e:
           print Exception,':',e
        readed['container']['docker']['image'] = createContainerServerModel.imagename
        name = readed['id'] 
        json.dump(readed, open('src/static/model/docker/app.json', 'w'))
        return 'ok'

if __name__ == '__main__':
    createContainerProfile()    
    