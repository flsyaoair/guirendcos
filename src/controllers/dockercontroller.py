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

@docker.route('/ServerModel/Delete',methods=['POST'])
def serverModelDelete():
    issueservice.delete(request.json['IssueId'])
    return jsonify(deleted=True)    
def serverModellist(servermodel_id):
    member_list = teamservice.member_in_project(servermodel_id)
    category = issueservice.available_category()
    return render_template('ServerModel/List.html',ProjectId=project_id,MemberList=member_list,Category=category)    


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

@docker.route('/ServerModel/Delete',methods=['POST'])
def resourceDelete():
    dockerservice.delete(request.json['IssueId'])
    return jsonify(deleted=True)    
def resourceModellist(servermodel_id):
    member_list = teamservice.member_in_project(servermodel_id)
    category = issueservice.available_category()
    return render_template('ServerModel/List.html',ProjectId=project_id,MemberList=member_list,Category=category)    


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
def query():
    subject = request.json['Subject']
    assign_to = int(request.json['AssignTo'])
    if assign_to == -1:
        assign_to = g.user_id
    category_id = int(request.json['CategoryId'])
    status_open = request.json['Open']
    status_fixed = request.json['Fixed']
    status_closed = request.json['Closed']
    status_canceled = request.json['Canceled']
    page_no = request.json['PageNo']
    (row_count,page_count,page_no,page_size,data) = issueservice.query(subject,assign_to,category_id,status_open,status_fixed,status_closed,status_canceled,'CreateDate',page_no,PAGESIZE_issue,g.user_id)
    issue_list = []
    for i in data.all():
        issue_list.append({'IssueId':i.IssueId,'ProjectId':i.ProjectId,'ProjectKey':i.ProjectProfile.ProjectKey,'Category':i.Category.CategoryName,'Subject':i.Subject,'Priority':i.Priority,'Status':i.Status,'AssignTo':i.AssignToProfile.Nick,'Creator':i.CreatorProfile.Nick,'LastUpdateDate':i.LastUpdateDate.isoformat()})
    return jsonify(row_count=row_count,page_count=page_count,page_no=page_no,page_size=page_size,data=issue_list)
    
if __name__ == '__main__':
    createContainerProfile()    
    