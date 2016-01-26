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
        json.dump(readed, open('src/static/model/docker/'+projectkey+'app.json', 'w'))
        dockerprofile=dict(resourcemodeldict, **servermodeldict)
        dockerprofile = str(dockerprofile)

#         eval(a)
        projectservice.create_project(projectname,projectkey,packagegettype,scmurl,poll,shell,status)
        projectservice.create_projectProfile(projectkey,dockerprofile)
        
        return jsonify(created=True)
    
    
@project.route('/App/Update',methods=['POST'])
def updateProjectProfile():
        projectkey = request.json['ProjectKey']
        imagename = request.json['ImageName']
        containerport = request.json['ContainerPort']    
        hostport = request.json['HostPort']
        containerpath = request.json['ContainerPath']
        hostpath = request.json['HostPath']
        
        case = request.json['Case']
        dockercpu = request.json['DockerCpu']
        dockermemory = request.json['DockerMemory']
        dockervolume = request.json['DockerVolume']
        resourcemodeldict = {"Case":case,"DockerCpu":dockercpu,"DockerMemory":dockermemory,"DockerVolume":dockervolume}
        servermodeldict = {"ImageName":imagename,"ContainerPort":containerport,"HostPort":hostport,"ContainerPath":containerpath,"HostPath":hostpath
        } 
        dockerprofile=dict(resourcemodeldict, **servermodeldict)
        dockerprofile = str(dockerprofile)
        projectservice.update_projectProfile(projectkey, dockerprofile)       
        return jsonify(updated=True)

@project.route('/App/Delete',methods=['POST'])
def deleteProject():
    dockerservice.serverModelDelete(request.json['ServerModelId'])
    return jsonify(deleted=True)    



if __name__ == '__main__':
    dockerservice.resourceModelList(1)
    dockerservice.serverModelList(1)   
    