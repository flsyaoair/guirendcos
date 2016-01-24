# -*- coding: UTF-8 -*- 
from src.models import dockerServerModel,dockerResourceModel,database
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
    docker = session.query(dockerServerModel).filter(dockerServerModel.ServiceModeld == servermodel_id).one()
    docker.ImageName = imagename
    docker.ContainerPort = containerport
    docker.HostPort = hostport
    docker.ContainerPath = containerpath
    docker.HostPath = hostpath
    docker.LastUpdateDate = datetime.now()  
    session.add(docker)
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