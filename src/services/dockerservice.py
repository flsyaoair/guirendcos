# -*- coding: UTF-8 -*- 
from src.models import database
from src.models.docker import dockerServerModel,dockerResourceModel
from datetime import datetime
# from configmanage.collect import mesoscollet
# cpus='1.0'
def create_dockerservermodel(nickname,imagetype,imagename,containerport,hostport,containerpath,hostpath):
    session = database.get_session()
    docker = dockerServerModel()
    docker.NickName = nickname
    docker.ImageType = imagetype
    docker.ImageName = imagename
    docker.ContainerPort = containerport
    docker.HostPort = hostport
    docker.ContainerPath = containerpath
    docker.HostPath = hostpath
    docker.CreateDate = datetime.now()  
    docker.LastUpdateDate = datetime.now() 
    session.add(docker)
    session.commit()
    session.close()
    
def update_dockerservermodel(servermodel_id,imagename,containerport,hostport,containerpath,hostpath):
    session = database.get_session()
    docker = session.query(dockerServerModel).filter(dockerServerModel.ServerModelId == servermodel_id).one()
    docker.ImageName = imagename
    docker.ContainerPort = containerport
    docker.HostPort = hostport
    docker.ContainerPath = containerpath
    docker.HostPath = hostpath
    docker.LastUpdateDate = datetime.now()  
    session.add(docker)
    session.commit()
    session.close()
    
def serverModelDelete(servermodel_id):
    session = database.get_session()
    docker = session.query(dockerServerModel).filter(dockerServerModel.ServerModelId == servermodel_id).delete()
    session.commit()
    session.close()   
#docker 资源模板         
def create_dockerresourcemodel(nickname,case,dockercpu,dockermemory,dockervolume):
    session = database.get_session()
    docker = dockerResourceModel()
    docker.NickName = nickname
    docker.Case = case
    docker.DockerCpu = dockercpu
    docker.DockerMemory = dockermemory
    docker.DockerVolume = dockervolume
    docker.CreateDate = datetime.now()
    docker.LastUpdateDate = datetime.now()  
    session.add(docker)
    session.commit()
    session.close() 
def update_dockerresourcemodel(resourcemodel_id,case,dockercpu,dockermemory,dockervolume):
    session = database.get_session()
    docker = session.query(dockerResourceModel).filter(dockerResourceModel.ResourceModelId == resourcemodel_id).one()
    docker.Case = case
    docker.DockerCpu = dockercpu
    docker.DockerMemory = dockermemory
    docker.DockerVolume = dockervolume
    docker.LastUpdateDate = datetime.now()  
    session.commit()
    session.close()
def resourceModelDelete(resourcemodel_id):
    session = database.get_session()
    docker = session.query(dockerResourceModel).filter(dockerResourceModel.ResourceModelId == resourcemodel_id).delete()
    session.commit()
    session.close() 
    
    
def query_serverModelList():
    session = database.get_session()
    servermodellist = session.query(dockerServerModel).all()
    session.close()
    return servermodellist   
    
def query_resourceModelList():
    session = database.get_session()
    resourcemodellist = session.query(dockerResourceModel).all()
    session.close()
    return resourcemodellist    

def serverModelList(servermodel_id):
    session = database.get_session()
    servermodellist = session.query(dockerServerModel).filter(dockerServerModel.ServerModelId == servermodel_id).one()
    session.close()
    return servermodellist   
    
def resourceModelList(resourcemodel_id):
    session = database.get_session()
    resourcemodellist = session.query(dockerResourceModel).filter(dockerResourceModel.ResourceModelId == resourcemodel_id).one()
    session.close()
    return resourcemodellist      